from bytecorecompiler.lexical_analysis import LexicalAnalysis


class TestLexicalAnalysis:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__parse__empty_input__returns_one_newline_token(self) -> None:
        # Arrange
        expected = ['\n']
        string = ''

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__line_input_with_comment__returns_three_tokens_and_a_newline(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n']
        string = '00 00 LOAD; Foobar'

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__line_input_with_two_comments__returns_three_tokens_and_a_newline(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n']
        string = '00 00 LOAD; Foobar; Foobar'

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__8_lines_input_with_comments__returns_32_tokens(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n', '00', '00', 'LOAD',
                    '\n', '00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n', '00', '00', 'LOAD', '\n']
        string = '00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n00 00 LOAD; Foobar\n'

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__line_input_with_trailing_spaces__returns_three_tokens_and_a_newline(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n']
        string = '00 00 LOAD  '

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__line_input_with_leading_spaces__returns_three_tokens_and_a_newline(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n']
        string = '  00 00 LOAD'

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected

    def test__parse__line_input_with_extra_spaces_in_between_tokens__returns_three_tokens_and_a_newline(self) -> None:
        # Arrange
        expected = ['00', '00', 'LOAD', '\n']
        string = '00  00  LOAD'

        lexical_analysis = LexicalAnalysis()

        # Act
        actual = lexical_analysis.parse(string)

        # Assert
        assert actual == expected
