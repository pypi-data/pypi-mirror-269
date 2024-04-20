from ast import AST, NodeVisitor, Attribute
from typing import Generator, Any, Tuple, Type

import importlib.metadata as importlib_metadata


class Visitor(NodeVisitor):
    def __init__(self):
        self.errors = {}
        self.dot_line = -1
        self.counter = 0

    def visit_Attribute(self, node: Attribute):
        if node.lineno != self.dot_line:
            self.dot_line = node.lineno
            self.counter = 0

        self.counter += 1
        if self.counter > 1:
            self.errors[self.dot_line] = [1, f'FOD100 Too many dots per line: {self.counter} dots found']
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: AST) -> None:
        self.tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self.tree)
        errors = visitor.errors
        for error in [(key, *value) for key, value in errors.items()]:
            yield error + (type(self),)
