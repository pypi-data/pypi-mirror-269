import ast

from dataclasses import dataclass, field

from transpiler.utils import UnsupportedNodeError, highlight


class NodeVisitorSeq:
    def visit(self, node):
        __TB__ = f"running type analysis on {highlight(node)}"
        """Visit a node."""
        if type(node) == list:
            for n in node:
                self.visit(n)
        else:
            for parent in node.__class__.__mro__:
                if visitor := getattr(self, 'visit_' + parent.__name__, None):
                    try:
                        return visitor(node)
                    except Exception as e:
                        raise
            else:
                self.missing_impl(node)

    def missing_impl(self, node):
        try:
            raise UnsupportedNodeError(str(node))
        except Exception as e:
            raise NotImplementedError(type(node))

@dataclass
class PlainBlock(ast.stmt):
    body: list[ast.stmt] = field(default_factory=lambda:[ast.parse('print("WTF")')])
    _fields = ("body",)
    __match_args__ = ("body",)
    _attributes = ("lineno", "col_offset", "end_lineno", "end_col_offset", "body")


@dataclass
class AnnotationName(ast.AST):
    inner: "transpiler.phases.typing.types.BaseType"

    @property
    def id(self):
        return str(self.inner)

AnnotationName.__name__ = "Name"

def make_lnd(op1, op2):
    return {
        "lineno": op1.lineno,
        "col_offset": op1.col_offset,
        "end_lineno": op2.end_lineno,
        "end_col_offset": op2.end_col_offset
    }