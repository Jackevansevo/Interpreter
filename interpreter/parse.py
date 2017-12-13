from collections import namedtuple
from itertools import chain, islice, repeat

from interpreter.node import Node

AstLine = namedtuple('AstLine', ['id', 'indent', 'contents'])


def parse_ast(ast):
    ast_lines = []

    # Parses contents and indentation level from each lines
    for index, line in enumerate(ast):
        contents = line.lstrip()
        indent = len(line) - len(contents)
        ast_lines.append(AstLine(index, indent, contents))

    return parse(ast_lines)


def get_next_indented(lines, current_level):
    next_indent = current_level + 2
    for line in lines:
        if line.indent == next_indent:
            yield line


def parse(lines):

    line, *rest = lines
    node = Node(line.contents)

    children = get_next_indented(rest, line.indent)

    lhs, rhs = islice(chain(children, repeat(None)), 2)

    if lhs:
        if rhs:
            node.lhs = parse(rest[:rest.index(rhs)])
        else:
            node.lhs = parse(rest[:len(lines)])
    else:
        node.lhs = None

    if rhs:
        node.rhs = parse(rest[rest.index(rhs):])
    else:
        node.rhs = None

    return node
