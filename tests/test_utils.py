from unittest.mock import patch
from tempfile import NamedTemporaryFile

from interpreter.interpret import make_ast, parse_ast
from interpreter.utils import line_count, draw_graph


def test_line_count():
    temp = NamedTemporaryFile()
    with open(temp.name, 'r+') as f:
        f.writelines(["far\n", "bar\n", "baz\n"])
        f.seek(0)
        assert line_count(f) == 3
