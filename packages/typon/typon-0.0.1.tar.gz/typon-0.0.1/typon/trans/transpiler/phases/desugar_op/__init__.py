# coding: utf-8
import ast

from transpiler.utils import linenodata

DUNDER = {
    ast.Mult: "mul",
    ast.Add: "add",
    ast.Sub: "sub",
    ast.Div: "truediv",
    ast.FloorDiv: "floordiv",
    ast.Mod: "mod",
    ast.LShift: "lshift",
    ast.RShift: "rshift",
    ast.BitXor: "xor",
    ast.BitOr: "or",
    ast.BitAnd: "and",
    ast.USub: "neg",
    ast.UAdd: "pos",
    ast.Invert: "invert"
}


class DesugarOp(ast.NodeTransformer):
    def visit_BinOp(self, node: ast.BinOp):
        lnd = linenodata(node)
        res = ast.Call(
            func=ast.Attribute(
                value=self.visit(node.left),
                attr=f"__{DUNDER[type(node.op)]}__",
                ctx=ast.Load(),
                **lnd
            ),
            args=[self.visit(node.right)],
            keywords={},
            **lnd
        )
        res.orig_node = node
        return res

    def visit_UnaryOp(self, node: ast.UnaryOp):
        lnd = linenodata(node)
        if type(node.op) == ast.Not:
            res = ast.UnaryOp(
                operand=self.visit(node.operand),
                op=node.op,
                **lnd
            )
        else:
            res = ast.Call(
                func=ast.Attribute(
                    value=self.visit(node.operand),
                    attr=f"__{DUNDER[type(node.op)]}__",
                    ctx=ast.Load(),
                    **lnd
                ),
                args=[],
                keywords={},
                **lnd
            )
        res.orig_node = node
        return res

    # def visit_AugAssign(self, node: ast.AugAssign):
    #     return
