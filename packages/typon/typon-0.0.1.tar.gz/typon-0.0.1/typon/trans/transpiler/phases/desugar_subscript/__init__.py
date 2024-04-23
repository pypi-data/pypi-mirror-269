# coding: utf-8
import ast

from transpiler.phases.utils import make_lnd
from transpiler.utils import linenodata


class DesugarSubscript(ast.NodeTransformer):
    def visit_Subscript(self, node: ast.Subscript):
        match node.ctx:
            case ast.Load():
                res = ast.Call(
                        func=ast.Attribute(
                            value=node.value,
                            attr="__getitem__",
                            ctx=ast.Load(),
                        ),
                        args=[node.slice],
                        keywords=[],
                        **linenodata(node)
                    )
            case ast.Store():
                return node
                # res = ast.Call(
                #     func=ast.Attribute(
                #         value=node.value,
                #         attr="__itemref__",
                #         ctx=ast.Load(),
                #     ),
                #     args=[node.slice],
                #     keywords=[],
                #     **linenodata(node)
                # )
            case ast.Del():
                raise NotImplementedError("Subscript deletion not supported")
            case _:
                raise ValueError(f"Unexpected context {node.ctx!r}", linenodata(node))
        res.orig_node = node
        return res