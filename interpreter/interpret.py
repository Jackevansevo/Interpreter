from attr import attrs, attrib
import argparse
import sys
from collections import namedtuple
from operator import add, eq, floordiv, ge, gt, le, lt, mod, mul, ne, sub
from subprocess import PIPE, STDOUT, run

from interpreter.frame import Frame
from interpreter.parse import parse_ast
from interpreter.utils import draw_graph, line_count

# [TODO] Get rid of horrible Global returns (perhaps store in Frame)

operators = {
    '+': add, '-': sub, '*': mul, '%': mod, '/': floordiv,
    '==': eq, '!=': ne, '>': gt, '<': lt, '>=': ge, '<=': le
}

# Function parameter type
Func = namedtuple('Func', ['node', 'env'])


@attrs
class ReturnObj:

    returning = attrib()
    ret_type = attrib()
    ret_val = attrib()


def interpret_tree(head):
    global Return
    Return = ReturnObj(False, None, None)
    recursive_interpret(head, Frame({}, {}))
    check_return_type(Return)
    return Return.ret_val


def interpret_if(node, environment):
    # Check if the if statement has an else clause
    predicate = recursive_interpret(node.lhs, environment)
    new_frame = Frame({}, environment)
    if node.rhs.tok.lexeme == "else":
        if predicate:
            return recursive_interpret(node.rhs.lhs, new_frame)
        else:
            return recursive_interpret(node.rhs.rhs, new_frame)
    else:
        if recursive_interpret(node.lhs, environment):
            return recursive_interpret(node.rhs, new_frame)


def interpret_return(node, environment):
    global Return
    Return.ret_val = recursive_interpret(node.lhs, environment)
    Return.returning = True


def interpret_function(node, environment):
    global Return
    # Save the functions node and current environment in the environment
    func = Func(node, environment)
    Return.type = node.return_type
    environment.bindings[node.lhs.rhs.lhs.tok.lexeme] = func

    # Check if function is main
    if node.lhs.rhs.lhs.tok.lexeme == "main":
        Return.ret_type = node.return_type
        return recursive_interpret(node.rhs, Frame({}, environment))
    else:
        # Avoid interpreting other functions
        return


def get_args_list(node, environment):
    if node.rhs:
        return [
            recursive_interpret(n, environment) for n in node.rhs.func_args
        ]


def check_args(func, params, args):
    # Checks length of arguments against function params
    if len(params) != len(args):
        func_name = func.lhs.rhs.lhs
        param_str = list(map(tuple, params))
        outlines = [
            f"Wrong number of arguments passed to func {func_name}",
            f"Expected: {len(params)} \n  {param_str}",
            f"Got {len(args)} \n  {args}"
        ]
        sys.exit('\n'.join(outlines))


def check_return_type(Return):
    if Return.ret_type == 'int' and not isinstance(Return.ret_val, int):
        outlines = [
            "Type Error:",
            f"  Expected {Return.ret_type}",
            f"  Given {type(Return.ret_val)}"
        ]
        sys.exit('\n'.join(outlines))


def interpret_apply(node, environment):

    global Return

    if node.lhs.tok.lexeme == "print":
        print(recursive_interpret(node.rhs, environment))
        return

    if node.lhs.tok.lexeme == "apply":
        # recursive_interpret the lhs of the apply
        func, env = recursive_interpret(node.lhs, environment)
    else:
        try:
            func, env = environment[node.lhs.tok.lexeme]
        except KeyError as error:
            sys.exit(f'NameError: func {error} undefined')

    args = get_args_list(node, environment) or []
    params = func.func_params

    check_args(func, params, args)

    # Create new environment for function with bindings from env
    bindings = {p.name: a for p, a in zip(params, args)}
    new_frame = Frame(bindings, env)

    Return.ret_type = func.return_type

    recursive_interpret(func.rhs, new_frame)

    if Return.returning:
        # if returning:
        Return.returning = False

    check_return_type(Return)
    return Return.ret_val


def interpret_operators(node, environment):
    return int(operators[node.tok.lexeme](
        recursive_interpret(node.lhs, environment),
        recursive_interpret(node.rhs, environment)
    ))


def interpret_binding(node, environment):
    # Initialize variables
    if node.lhs.tok.lexeme == "int" and node.rhs.tok.lexeme != "=":
        environment.bindings[node.rhs.tok.lexeme] = 0
    recursive_interpret(node.lhs, environment)
    return recursive_interpret(node.rhs, environment)


def interpret_assingment(node, environment):
    # Handle assingments
    rhs = recursive_interpret(node.rhs, environment)
    environment[node.lhs.tok.lexeme] = rhs


def default_interpret(node, environment):
    recursive_interpret(node.lhs, environment)
    return recursive_interpret(node.rhs, environment)


cases = {
    ';': default_interpret,
    '~': interpret_binding,
    '=': interpret_assingment,
    'D': interpret_function,
    'if': interpret_if,
    'apply': interpret_apply,
    'return': interpret_return,
}


def recursive_interpret(node, environment):

    global Return

    if Return.returning:
        return

    if node.is_leaf:

        if node.tok.lexeme == "int":
            return

        # Return underlying value of a constant
        elif node.tok.is_constant:
            return node.tok.val

        # Else check the environment
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
            sys.exit(f"Unrecognised token: {node.tok}")


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
        sys.exit(output)

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
    sys.exit(Return.ret_val)
