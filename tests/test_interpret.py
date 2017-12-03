import pytest
import re
from glob import glob

from interpreter.node import Node
from interpreter.token import Token
from interpreter.interpret import make_ast, interpret_tree
from interpreter.parse import parse_ast

HEADER_REGEX = re.compile(r"\/\*\s*(Answer|Error):\s*(.*)\s*\*\/")


def test_files():
    for fname in glob('examples/*.cmm'):
        with open(fname) as f:
            head = f.readline().strip()
            match = HEADER_REGEX.match(head)
            if match:
                f.seek(0)
                print(f.name)
                category, expected = match.groups()
                if category == "Answer":
                    result = interpret_tree(parse_ast(make_ast(f)))
                    assert str(result) == expected.strip(), f"{fname}"
                elif category == "Error":
                    with pytest.raises(SystemExit) as error:
                        interpret_tree(parse_ast(make_ast(f)))
                    assert expected.strip() in str(error.value)


def test_print(capsys):
    with open('examples/print.cmm') as f:
        interpret_tree(parse_ast(make_ast(f)))
        out, err = capsys.readouterr()
    assert out.strip() == "10"


def test_interpret_unrecognised_token():
    leaf = Node()
    leaf.tok = Token('~')
    head = Node()
    head.tok, head.lhs, head.rhs = Token('£'), leaf, None
    with pytest.raises(SystemExit) as error:
        interpret_tree(head)
    assert str(error.value) == "Unrecognised token: £"
