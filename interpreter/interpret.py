import argparse
import sys
from collections import ChainMap, deque, namedtuple
from operator import add, mod, mul, sub, truediv
from subprocess import PIPE, STDOUT, run

from interpreter.parse import parse_ast
from interpreter.utils import draw_graph, line_count

# Function parameter type
Param = namedtuple('Param', ['type', 'name'])
Func = namedtuple('Func', ['environment', 'signature', 'body'])


def interpret(node, environment):

    current_frame = next(iter(environment))

    if node.tok == "return":
        return interpret(node.lhs, environment)

    if node.tok == "if":

        # Check if the if statement has an else clause
        if node.rhs.tok == "else":
            if interpret(node.lhs, environment):
                return interpret(node.rhs.lhs, environment)
            else:
                return interpret(node.rhs.rhs, environment)
        else:
            if interpret(node.lhs, environment):
                return interpret(node.rhs, environment)
            else:
                return

    if node.tok == "D":
        # [TODO] Save the current environment and store it alongside the node
        current_frame[node.lhs.rhs.lhs.tok] = node
        # Check if function is main
        if node.lhs.rhs.lhs.tok == "main":
            interpret(node.lhs, environment)
            return interpret(node.rhs, environment)
        else:
            return

    if node.tok == "apply":
        try:
            func = ChainMap(*environment).get(node.lhs.tok)
        except KeyError as error:
            sys.exit(f'NameError: func {error} undefined')
        else:
            # Check if function takes arguments
            if not func.lhs.rhs.rhs:
                # Create a new environment frame
                return interpret(func.rhs, deque([{}]))

            # Handle arguments
            args = [interpret(l, environment) for l in node.rhs.leaf_children]

            fn_nodes = [leaf.tok for leaf in func.lhs.rhs.rhs.leaf_children]
            params = [Param(*p) for p in zip(fn_nodes[::2], fn_nodes[1::2])]

            # Checks length of arguments against function params
            if len(params) != len(args):
                func_name = func.lhs.rhs.lhs
                print(f"Wrong number of arguments passed to func {func_name}")
                param_str = list(map(tuple, params))
                print("Expected:", len(params), "\n ", param_str)
                print("Got:", len(args), "\n ", args)
                sys.exit(1)

            # Basic type checking
            for param, arg in zip(params, args):
                if param.type == "int" and not isinstance(arg, int):
                    print("Type Error")
                    print(f"Expected: {param.type}")
                    print(f"Given {arg}")
                    sys.exit(1)

            func_environment = {p.name: a for p, a in zip(params, args)}
            # Merge current frame with new function environment
            current_frame = {**current_frame, **func_environment}
            return interpret(func.rhs, deque([current_frame]))

    if node.is_leaf:

        # Skip builtins
        if node.tok in {"int", "F"}:
            return node.tok

        # If token is a digit
        if node.is_constant:
            return node.val

        if node.is_identifier:
            var = ChainMap(*environment).get(node.tok)
            if var is None:
                sys.exit(f"{node.tok} Undefined")
            return var

        return node.tok

    # Handle equality
    if node.tok == "==":
        lhs = interpret(node.lhs, environment)
        rhs = interpret(node.rhs, environment)
        # Cast boolean to an integer
        return int(lhs == rhs)

    if node.tok == "=":
        rhs = interpret(node.rhs, environment)
        current_frame[node.lhs.tok] = interpret(node.rhs, environment)
        return

    # Handle maths operators
    operators = {'+': add, '-': sub, '*': mul, '%': mod, '/': truediv}
    if node.tok in operators.keys():
        return operators.get(node.tok)(
            interpret(node.lhs, environment), interpret(node.rhs, environment)
        )

    interpret(node.lhs, environment)
    return interpret(node.rhs, environment)


def parse_args():
    parser = argparse.ArgumentParser(description='Interprets a script.')
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--graph', action='store_true')
    args = parser.parse_args()
    return args


def make_ast(f):
    cmd = f"./mycc < {f.name}"

    out = run(cmd, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

    output = out.stdout.decode('utf-8')
    outlines = output.splitlines()

    if outlines[-1] == 'syntax error':
        # Exit if syntax error encountered
        sys.stdout.write(output)
        sys.exit(1)

    ast = outlines[line_count(f):]

    return ast


def interpret_file(fname):
    with open(fname) as f:
        return interpret_node(parse_ast(make_ast(f)))


def interpret_node(node):
    # Environment is a queue of frames
    environment = deque([{}])
    return interpret(node, environment)


if __name__ == '__main__':

    args = parse_args()

    ast = make_ast(args.file)

    if args.debug:
        for line in ast:
            print(line)

    head = parse_ast(ast)

    if args.graph:
        draw_graph(head)

    print(interpret_node(head))
