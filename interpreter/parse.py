from collections import namedtuple
from operator import attrgetter
from itertools import chain, islice, repeat


class Node:

    def __str__(self):
        return self.tok

    def __repr__(self):
        return f'<Node(tok={self.tok})>'

    def __iter__(self):
        if self.lhs:
            yield from self.lhs
        yield self
        if self.rhs:
            yield from self.rhs

    @property
    def leaf_children(self):
        return filter(attrgetter('is_leaf'), iter(self))

    @property
    def is_identifier(self):
        return self.tok.isalpha()

    @property
    def is_constant(self):
        return self.tok.isdigit()

    @property
    def is_leaf(self):
        return not all([self.lhs, self.rhs])


def parse_ast(ast):
    AstLine = namedtuple('AstLine', ['id', 'indent', 'tok'])
    ast_lines = []

    for index, line in enumerate(ast):
        tok = line.lstrip()
        indent = len(line) - len(tok)
        ast_lines.append(AstLine(index, indent, tok))

    return parse(ast_lines)


def get_next_indented(nodes, head):
    next_indent = head.indent + 2
    for node in nodes:
        if node.indent == next_indent:
            yield node


def parse(nodes):

    head, *rest = nodes
    node = Node()

    node.tok = head.tok

    # Store integer values
    if node.tok.isdigit():
        node.val = int(node.tok)
    else:
        node.val = None

    children = get_next_indented(rest, head)

    lhs, rhs = islice(chain(children, repeat(None)), 2)

    if lhs:
        if rhs:
            node.lhs = parse(rest[:rest.index(rhs)])
        else:
            node.lhs = parse(rest[:len(nodes)])
    else:
        node.lhs = None

    if rhs:
        node.rhs = parse(rest[rest.index(rhs):])
    else:
        node.rhs = None

    return node
