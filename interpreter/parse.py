from collections import namedtuple
from itertools import chain, islice, repeat

from interpreter.node import Node
from interpreter.token import Token

AstLine = namedtuple('AstLine', ['id', 'indent', 'tok'])


def parse_ast(ast):
    ast_lines = []

    # Parses token and indentation level from each lines
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

    node.tok = Token(head.tok)

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
