# coding: utf-8
import ast

from transpiler.phases.utils import PlainBlock


def process(items: list[ast.withitem], body: list[ast.stmt]) -> PlainBlock:
    first, *rest = items
    val, name = first.context_expr, first.optional_vars
    cm_name = ast.Name(id=f"cm_{hash(first)}")
    end_node = name or first.context_expr
    with_lineno = {"lineno": first.context_expr.lineno, "col_offset": first.context_expr.col_offset,
                   "end_lineno": end_node.end_lineno, "end_col_offset": end_node.end_col_offset}
    res = [
        ast.Assign(targets=[cm_name], value=val, **with_lineno)
    ]
    enter_call = ast.Call(func=ast.Attribute(value=cm_name, attr="__enter__", **with_lineno), args=[], keywords=[],
                          **with_lineno)
    if name:
        res.append(ast.Assign(targets=[name], value=enter_call, **with_lineno))
    else:
        res.append(ast.Expr(value=enter_call, **with_lineno))
    if rest:
        res.append(process(rest, body))
    else:
        res.append(PlainBlock(body))
    res.append(ast.Expr(
        value=ast.Call(func=ast.Attribute(value=cm_name, attr="__exit__"), args=[], keywords=[], **with_lineno)))
    return PlainBlock(res)


class DesugarWith(ast.NodeTransformer):
    def visit_With(self, node: ast.With):
        return process(
            list(map(self.visit, node.items)),
            list(map(self.visit, node.body))
        )
