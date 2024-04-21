from bytecorecompiler.syntax_tree import SyntaxTree


class TestSyntaxTree:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__init__instantiating_syntax_tree__does_not_raise_exception(self) -> None:
        # Arrange
        msb = '00'
        lsb = '00'
        opcode = 'LOAD'
        linenumber = 1

        SyntaxTree(msb, lsb, opcode, linenumber)

    def test__linenumber__init_syntax_tree__returns_correct_linenumber(self) -> None:
        # Arrange
        expected = 1
        msb = '00'
        lsb = '00'
        opcode = 'LOAD'
        linenumber = 1

        syntax_tree = SyntaxTree(msb, lsb, opcode, linenumber)

        # Act
        actual = syntax_tree.linenumber

        # Assert
        assert actual == expected

    def test__linenumber__init_syntax_tree_with_no_linenumber__returns_correct_linenumber(self) -> None:
        # Arrange
        expected = None
        msb = '00'
        lsb = '00'
        opcode = 'LOAD'
        linenumber = None

        syntax_tree = SyntaxTree(msb, lsb, opcode, linenumber)

        # Act
        actual = syntax_tree.linenumber

        # Assert
        assert actual == expected

    def test__data__init_syntax_tree_with_opcode__returns_correct_data(self) -> None:
        # Arrange
        expected = '01'
        msb = '00'
        lsb = '00'
        opcode = 'LOAD'
        linenumber = 1

        syntax_tree = SyntaxTree(msb, lsb, opcode, linenumber)
        syntax_tree.validate()

        # Act
        actual = syntax_tree.data

        # Assert
        assert actual == expected
