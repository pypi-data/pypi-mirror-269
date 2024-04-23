import pytest
from bytecorecompiler.syntax_analysis import SyntaxAnalysis, WrongNumberOfTokens, SyntaxAnalysisException, SyntaxAnalysisError


class TestSyntaxAnalysis:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__parse__one_line_of_valid_tokens__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['00', '00', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__one_line_of_valid_byte_tokens__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['00', '00', '00', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__another_one_line_of_valid_byte_tokens__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['00', '00', 'ff', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__newline_token__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__no_tokens__raises_wrong_number_of_tokens(self) -> None:
        # Arrange
        tokens: list[str] = []

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(WrongNumberOfTokens) as e:
            syntax_analysis.parse(tokens)
        assert e.type is WrongNumberOfTokens
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Wrong number of tokens on line: 1.'

    def test__parse__one_line_of_invalid_number_of_tokens__raises_wrong_number_of_tokens(self) -> None:
        # Arrange
        tokens: list[str] = ['00']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(WrongNumberOfTokens) as e:
            syntax_analysis.parse(tokens)
        assert e.type is WrongNumberOfTokens
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Wrong number of tokens on line: 1.'

    def test__parse__two_lines_of_tokens_second_is_invalid__raises_wrong_number_of_tokens(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', '00', '00', 'LOAD', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(WrongNumberOfTokens) as e:
            syntax_analysis.parse(tokens)
        assert e.type is WrongNumberOfTokens
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Wrong number of tokens on line: 2.'

    def test__parse__two_lines_of_valid_tokens__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__8_lines_of_valid_tokens__does_not_raise_exception(self) -> None:
        # Arrange
        tokens = ['\n', '\n', '00', '00', 'LOAD', '\n',
                  '00', '00', 'LOAD', '\n', '\n', '\n', '\n', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        syntax_analysis.parse(tokens)

    def test__parse__two_lines_and_msb_invalid_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', 'Foobar', '00', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid MSB length on line: 2.'

    def test__parse__two_lines_and_lsb_invalid_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', '00', 'Foobar', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid LSB length on line: 2.'

    def test__parse__two_lines_and_opcode_invalid_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', '00', '00', 'Foobar', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid OPCODE on line: 2.'

    def test__parse__two_lines_and_msb_invalid_byte_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', 'ZZ', '00', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid MSB byte on line: 2.'

    def test__parse__two_lines_and_lsb_invalid_byte_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', '00', 'ZZ', 'LOAD', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid LSB length on line: 2.'

    def test__parse__two_lines_and_opcode_invalid_byte_on_second_line__raises_syntax_analysis_error(self) -> None:
        # Arrange
        tokens: list[str] = ['00', '00', 'LOAD',
                             '\n', '00', '00', 'ZZ', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act and assert
        with pytest.raises(SyntaxAnalysisError) as e:
            syntax_analysis.parse(tokens)
        assert e.type is SyntaxAnalysisError
        assert issubclass(e.type, SyntaxAnalysisException)
        assert e.value.args[0] == 'Syntax error: Invalid DATA on line: 2.'

    def test__parse__8_lines_of_valid_tokens__returns_8_syntax_trees(self) -> None:
        # Arrange
        expected = 8
        tokens = ['\n', '\n', '00', '00', 'LOAD', '\n',
                  '00', '00', 'LOAD', '\n', '\n', '\n', '\n', '\n']

        syntax_analysis = SyntaxAnalysis()

        # Act
        syntax_trees = syntax_analysis.parse(tokens)
        actual = len(syntax_trees)

        # Assert
        assert actual == expected
