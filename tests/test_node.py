from interpreter.parse import parse_ast

Tree = str.splitlines


def test_return_type():
    """
    Checks that return_type returns the correct value from function signatures
    """
    tree = Tree("""
    D
      d
        int
        F
          example
      return
        5
    """)
    node = parse_ast(tree[1:])
    assert node.return_type == 'int'

    # Check that non function type nodes have no return type
    node = parse_ast('+')
    assert not node.return_type


def test_has_branches():
    """Checks that has branches returns true is node has both a lhs and rhs"""
    tree = Tree("""
    +
      1
      2
    """)
    head = parse_ast(tree[1:])
    assert head.has_branches

    tree = Tree("""
    return
      0
    """)
    head = parse_ast(tree[1:])
    assert not head.has_branches


def test_is_func():
    tree = Tree("""
    D
      d
        int
        F
          example
      return
        5
    """)
    head = parse_ast(tree[1:])
    assert head.is_func

    head = parse_ast('+')
    assert not head.is_func


def test_str():
    head = parse_ast('D')
    assert str(head) == 'D'
