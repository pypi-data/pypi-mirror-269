import ast

from transpiler.utils import compare_ast

NAME_MAIN = ast.parse('__name__ == "__main__"', mode="eval").body

class IfMainVisitor(ast.NodeVisitor):
    def visit_Module(self, node: ast.Module):
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.If):
                if not stmt.orelse and compare_ast(stmt.test, NAME_MAIN):
                    new_node = ast.parse("def main(): pass").body[0]
                    new_node.body = stmt.body
                    new_node.is_main = True
                    node.main_if = new_node
                    node.body[i] = new_node
                    return