from interpreter.token import Token


def test_val():

    tok = Token('1')
    assert tok.val == 1

    tok = Token('x')
    assert not tok.val


def test_is_temporary():
    tok = Token('t1')
    assert tok.is_temporary

    tok = Token('x')
    assert not tok.is_temporary


def test_str():
    tok = Token('1')
    assert str(tok) == '1'
