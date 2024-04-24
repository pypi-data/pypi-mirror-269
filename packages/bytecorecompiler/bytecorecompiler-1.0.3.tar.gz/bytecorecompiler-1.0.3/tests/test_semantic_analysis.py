import pytest
from bytecorecompiler.semantic_analysis import SemanticAnalysis, SemanticAnalysisException, DuplicateMemoryAddressAssignment, MissingExtendedMemoryAddress
from bytecorecompiler.syntax_tree import SyntaxTree


class TestSemanticAnalysis:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__parse__two_lines_assigning_to_same_memory_address__raises_duplicate_memory_address_assignment(self) -> None:
        # Arrange
        syntax_trees: list[SyntaxTree] = [
            SyntaxTree('00', '00', 'LOAD', 1),
            SyntaxTree('00', '00', 'LOAD', 2),
        ]
        for syntax_tree in syntax_trees:
            syntax_tree.validate()

        semantic_analysis = SemanticAnalysis()

        # Act and assert
        with pytest.raises(DuplicateMemoryAddressAssignment) as e:
            semantic_analysis.parse(syntax_trees)
        assert e.type is DuplicateMemoryAddressAssignment
        assert issubclass(e.type, SemanticAnalysisException)
        assert e.value.args[0] == 'Memory address has already been assigned to on line: 2.'

    def test__parse__opcode_with_no_msb_and_no_lsb__raises_missing_extended_memory_address(self) -> None:
        # Arrange
        syntax_trees: list[SyntaxTree] = [
            SyntaxTree('00', '00', 'LOAD', 1),
        ]
        for syntax_tree in syntax_trees:
            syntax_tree.validate()

        semantic_analysis = SemanticAnalysis()

        # Act and assert
        with pytest.raises(MissingExtendedMemoryAddress) as e:
            semantic_analysis.parse(syntax_trees)
        assert e.type is MissingExtendedMemoryAddress
        assert issubclass(e.type, SemanticAnalysisException)
        assert e.value.args[0] == 'Missing extended memory address after OPCODE on line: 1.'

    def test__parse__opcode_with_msb_and_lsb__does_not_raise_exception(self) -> None:
        # Arrange
        syntax_trees: list[SyntaxTree] = [
            SyntaxTree('00', '00', 'LOAD', 1),
            SyntaxTree('00', '01', '00', 2),
            SyntaxTree('00', '02', '00', 3),
        ]
        for syntax_tree in syntax_trees:
            syntax_tree.validate()

        semantic_analysis = SemanticAnalysis()

        # Act and assert
        semantic_analysis.parse(syntax_trees)

    def test__parse__opcode_is_missing_valid_msb_byte__raises_missing_extended_memory_address(self) -> None:
        # Arrange
        syntax_trees: list[SyntaxTree] = [
            SyntaxTree('00', '00', 'LOAD', 1),
            SyntaxTree('00', '01', 'LOAD', 2),
            SyntaxTree('00', '02', '00', 3),
            SyntaxTree('00', '03', '00', 4),
        ]
        for syntax_tree in syntax_trees:
            syntax_tree.validate()

        semantic_analysis = SemanticAnalysis()

        # Act and assert
        with pytest.raises(MissingExtendedMemoryAddress) as e:
            semantic_analysis.parse(syntax_trees)
        assert e.type is MissingExtendedMemoryAddress
        assert issubclass(e.type, SemanticAnalysisException)
        assert e.value.args[0] == 'Missing extended memory address after OPCODE on line: 1.'

    def test__parse__empty_syntax_trees__returns_empty_list_of_syntax_trees(self) -> None:
        # Arrange
        expected: list[SyntaxTree] = []
        syntax_trees: list[SyntaxTree] = [
            SyntaxTree(None, None, None, 1),
            SyntaxTree(None, None, None, 2),
            SyntaxTree(None, None, None, 3),
            SyntaxTree(None, None, None, 4),
        ]
        for syntax_tree in syntax_trees:
            syntax_tree.validate()

        semantic_analysis = SemanticAnalysis()

        # Act
        actual = semantic_analysis.parse(syntax_trees)

        # Assert
        assert actual == expected
