from interpreter.interpret import interpret_file


def test_operators():
    assert interpret_file('examples/operators.cmm') == 2


def test_scope():
    assert interpret_file('examples/scope.cmm') == 5


def test_functions():
    assert interpret_file('examples/function.cmm') == 7


def test_conditionals():
    assert interpret_file('examples/if_statement.cmm') == 1
    assert interpret_file('examples/if_else_statement.cmm') == 1
