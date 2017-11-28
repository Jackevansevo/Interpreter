from interpreter.frame import Frame


def test_getitem():
    glob = Frame({'x': 2}, None)
    frame = Frame({'y': 3}, glob)
    assert frame.get('x') == 2


def test_setitem():
    glob = Frame({'x': 2}, None)
    glob['x'] = 3
    assert glob['x'] == 3


def test_overrides_parent_scope():
    glob = Frame({'x': 2}, None)
    child = Frame({}, glob)
    child['x'] = 3
    assert glob['x'] == 3
    child['b'] = 3
    assert not glob.get('b')


def test_get():
    glob = Frame({'x': 2}, None)
    Frame({'y': 2, 'a': 3}, glob)
    assert not glob.get('z')


def test_str():
    assert str(Frame({'x': 2}, None)) == "{'x': 2}"
