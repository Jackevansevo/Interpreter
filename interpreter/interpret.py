import argparse
import sys
from collections import namedtuple
from operator import add, eq, floordiv, ge, gt, le, lt, mod, mul, ne, sub
from subprocess import PIPE, STDOUT, run

from interpreter.frame import Frame
from interpreter.parse import parse_ast
from interpreter.utils import draw_graph, line_count

operators = {
    '+': add, '-': sub, '*': mul, '%': mod, '/': floordiv,
    '==': eq, '!=': ne, '>': gt, '<': lt, '>=': ge, '<=': le
}

ret_val = None
returning = False

# Function parameter type
Func = namedtuple('Func', ['node', 'env'])


def interpret_tree(head):
    # Reset globals
    global returning
    global ret_val
    returning = False
    ret_val = None
    interpret(head, Frame({}, {}))
    return ret_val


def interpret_if(node, environment):
    # Check if the if statement has an else clause
    predicate = interpret(node.lhs, environment)

    if node.rhs.tok.lexeme == "else":
        if predicate:
            return interpret(node.rhs.lhs, Frame({}, environment))
        else:
            return interpret(node.rhs.rhs, Frame({}, environment))
    else:
        if interpret(node.lhs, environment):
            return interpret(node.rhs, Frame({}, environment))
        else:
            return


def interpret_return(node, environment):
    global returning
    global ret_val
    ret_val = interpret(node.lhs, environment)
    returning = True
    return


def interpret_function(node, environment):
    # Save the functions node and current environment in the environment
    func = Func(node, environment)
    environment.bindings[node.lhs.rhs.lhs.tok.lexeme] = func

    # Check if function is main
    if node.lhs.rhs.lhs.tok.lexeme == "main":
        return interpret(node.rhs, Frame({}, environment))
    else:
        # Avoid interpreting other functions
        return


def interpret_apply(node, environment):

    global returning
    global ret_val

    if node.lhs.tok.lexeme == "print":
        print(interpret(node.rhs, environment))
        return

    try:
        func, env = environment[node.lhs.tok.lexeme]
    except KeyError as error:
        sys.exit(f'NameError: func {error} undefined')
    else:
        if node.rhs:
            args = [interpret(n, environment) for n in node.rhs.func_args]
        else:
            args = []
        params = func.func_params

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

        bindings = {p.name: a for p, a in zip(params, args)}
        # Create new environment for function with bindings from env
        new_frame = Frame(bindings, environment[node.lhs.tok.lexeme].env)
        interpret(func.rhs, new_frame)
        if returning:
            returning = False
        return_type = func.lhs.lhs.tok.lexeme
        if return_type == 'int' and not isinstance(ret_val, int):
            print("Type Error")
            print(f"Expected: {return_type}")
            print(f"Given {type(ret_val)}")
            sys.exit(1)
        return ret_val


def interpret_operators(node, environment):
    return int(operators[node.tok.lexeme](
        interpret(node.lhs, environment),
        interpret(node.rhs, environment)
    ))


def interpret_binding(node, environment):
    # Initialize variables
    if node.lhs.tok.lexeme == "int" and node.rhs.tok.lexeme != "=":
        environment.bindings[node.rhs.tok.lexeme] = 0
    elif node.lhs.tok.lexeme == "function":
        environment.bindings[node.rhs.tok.lexeme] = (None, None)
    interpret(node.lhs, environment)
    return interpret(node.rhs, environment)


def interpret_assingment(node, environment):
    # Handle assingments
    rhs = interpret(node.rhs, environment)
    environment[node.lhs.tok.lexeme] = rhs


def default_interpret(node, environment):
    interpret(node.lhs, environment)
    return interpret(node.rhs, environment)


cases = {
    ';': default_interpret,
    '=': interpret_assingment,
    'D': interpret_function,
    'apply': interpret_apply,
    'if': interpret_if,
    'return': interpret_return,
    '~': interpret_binding,
}


def interpret(node, environment):

    global returning
    global ret_val

    if returning:
        return

    if node.is_leaf:

        if node.tok.lexeme == "int":
            return

        # Return underlying value of a constant
        if node.tok.is_constant:
            return node.tok.val

        if node.tok.is_identifier:
            var = environment.get(node.tok.lexeme)
            if var is None:
                sys.exit(f"{node.tok} Undefined")
            return var

    # Handle maths operators
    elif node.tok.lexeme in operators:
        return interpret_operators(node, environment)

    else:
        interpret_case = cases.get(node.tok.lexeme)
        if interpret_case:
            return interpret_case(node, environment)
        else:
            raise Exception(f"Unrecognised token: {node.tok}")


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


def main():

    args = parse_args()

    ast = make_ast(args.file)

    if args.debug:
        for line in ast:
            print(line)

    head = parse_ast(ast)

    if args.graph:
        draw_graph(head)

    interpret_tree(head)

    # Exit with correct status code
    sys.exit(ret_val)
