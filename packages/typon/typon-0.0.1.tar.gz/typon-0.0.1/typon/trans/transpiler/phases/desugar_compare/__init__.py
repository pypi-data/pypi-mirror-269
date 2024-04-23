# coding: utf-8
import ast

from transpiler.phases.utils import make_lnd
from transpiler.utils import linenodata

DUNDER = {
    ast.Eq: "eq",
    ast.Is: "eq",  # TODO
    ast.NotEq: "ne",
    ast.IsNot: "ne",  # TODO
    ast.Lt: "lt",
    ast.Gt: "gt",
    ast.GtE: "ge",
    ast.LtE: "le",
    ast.In: "contains",
    ast.NotIn: "contains",
}

class DesugarCompare(ast.NodeTransformer):
    def visit_Compare(self, node: ast.Compare):
        res = ast.BoolOp(ast.And(), [], **linenodata(node))
        operands = list(map(self.visit, [node.left, *node.comparators]))
        for left, op, right in zip(operands, node.ops, operands[1:]):
            lnd = make_lnd(left, right)
            if type(op) in (ast.In, ast.NotIn):
                left, right = right, left
            call = ast.Call(
                ast.Attribute(left, f"__{DUNDER[type(op)]}__", **lnd),
                [right],
                [],
                **lnd
            )
            if type(op) in (ast.NotIn, ast.IsNot):
                call = ast.UnaryOp(ast.Not(), call, **lnd)
            if type(op) not in (ast.In, ast.NotIn):
                call.orig_node = ast.Compare(left, [op], [right], **lnd)
            res.values.append(call)
        if len(res.values) == 1:
            res = res.values[0]
        return res