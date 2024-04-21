import pytest
from bytecorecompiler.parser import Parser
from bytecorecompiler.semantic_analysis import SemanticAnalysisException, MissingExtendedMemoryAddress


class TestParser:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__init__empty_input__does_not_raise_exception(self) -> None:
        # Arrange
        string = ''

        # Act and assert
        Parser(string)

    def test__init__one_full_opcode__does_not_raise_exception(self) -> None:
        # Arrange
        string = '00 00 LOAD; Foobar\n00 01 00\n00 02 00'

        # Act and assert
        Parser(string)

    def test__init__two_full_opcodes__does_not_raise_exception(self) -> None:
        # Arrange
        string = ''\
            + '00 00 LOAD;\n'\
            + '00 01 00\n'\
            + '00 02 00\n'\
            + '00 03 STORE; Foobar\n'\
            + '00 04 00; Foo\n'\
            + '00 05 00; Bar'

        # Act and assert
        Parser(string)

    def test__init__input_with_missing_extended_memory_address__raises_missing_extended_memory_address_on_expected_linenumber(self) -> None:
        # Arrange
        string = ''\
            + '\n\n\n'\
            + '00 00 LOAD\n'

        # Act and assert
        with pytest.raises(MissingExtendedMemoryAddress) as e:
            Parser(string)
        assert e.type is MissingExtendedMemoryAddress
        assert issubclass(e.type, SemanticAnalysisException)
        assert e.value.args[0] == 'Missing extended memory address after OPCODE on line: 4.'
