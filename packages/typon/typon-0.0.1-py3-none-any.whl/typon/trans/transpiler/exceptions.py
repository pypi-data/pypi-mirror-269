import ast
from abc import ABC


class CompileError(Exception, ABC):
    def detail(self, last_node: ast.AST = None) -> str:
        return ""
