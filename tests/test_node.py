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
