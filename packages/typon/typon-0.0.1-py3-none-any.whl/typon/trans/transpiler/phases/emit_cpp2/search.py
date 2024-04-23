# coding: utf-8
import ast

from transpiler.phases.emit_cpp import NodeVisitor


class SearchVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        yield from self.visit(item)
            elif isinstance(value, ast.AST):
                yield from self.visit(value)

    def match(self, node) -> bool:
        if type(node) == list:
            return any(self.match(n) for n in node)
        return next(self.visit(node), False)
