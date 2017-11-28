import re
from glob import glob

from interpreter.interpret import make_ast, parse_ast, interpret_tree

ANSWER_REGEX = re.compile(r"\/\*\s*Answer:\s*(\d*)\s*\*\/")


def test_files():
    for fname in glob('examples/*.cmm'):
        with open(fname) as f:
            head = f.readline().strip()
            match = ANSWER_REGEX.match(head)
            if match:
                expected = match.group(1)
                f.seek(0)
                result = interpret_tree(parse_ast(make_ast(f)))
                assert str(result) == expected, f"{fname}"
