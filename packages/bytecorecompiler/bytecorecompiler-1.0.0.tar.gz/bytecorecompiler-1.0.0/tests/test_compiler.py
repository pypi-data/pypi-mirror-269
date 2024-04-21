from bytecore.memory import Memory
from bytecore.memory_bytes_builder import MemoryBytesBuilder
from bytecorecompiler.compiler import Compiler


class TestCompiler:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__get_memory_bytes__no_input__gets_expected_memory_bytes(self) -> None:
        # Arrange
        memory_bytes = Memory.get_default_memory_bytes()
        expected = memory_bytes

        string = ''

        # Act
        compiler = Compiler(string)
        actual = compiler.get_memory_bytes()

        # Assert
        assert actual == expected

    def test__get_memory_bytes__two_full_opcodes__gets_expected_memory_bytes(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder()\
            .msb('00').lsb('00').data('01')\
            .msb('00').lsb('01').data('00')\
            .msb('00').lsb('02').data('00')\
            .msb('00').lsb('03').data('02')\
            .msb('00').lsb('04').data('00')\
            .msb('00').lsb('05').data('00')\
            .build()

        string = ''\
            + '00 00 LOAD;\n'\
            + '00 01 00\n'\
            + '00 02 00\n'\
            + '00 03 STORE; Foobar\n'\
            + '00 04 00; Foo\n'\
            + '00 05 00; Bar'

        # Act
        compiler = Compiler(string)
        actual = compiler.get_memory_bytes()

        # Assert
        assert actual == expected

    def test__get_memory_bytes__simple_example_program__gets_expected_memory_bytes(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder()\
            .msb('00').lsb('00').load()\
            .msb('00').lsb('01').data('00')\
            .msb('00').lsb('02').data('0A')\
            .msb('00').lsb('03').add()\
            .msb('00').lsb('04').data('00')\
            .msb('00').lsb('05').data('0B')\
            .msb('00').lsb('06').store()\
            .msb('00').lsb('07').data('FF')\
            .msb('00').lsb('08').data('FF')\
            .msb('00').lsb('09').halt()\
            .msb('00').lsb('0A').data('14').comment('20')\
            .msb('00').lsb('0B').data('1E').comment('30')\
            .build()

        string = ''\
            + '00 00 LOAD\n'\
            + '00 01 00\n'\
            + '00 02 0A\n'\
            + '00 03 ADD\n'\
            + '00 04 00\n'\
            + '00 05 0B\n'\
            + '00 06 STORE\n'\
            + '00 07 FF\n'\
            + '00 08 FF\n'\
            + '00 09 HALT\n'\
            + '00 0A 14; 20\n'\
            + '00 0B 1E; 30\n'

        # Act
        compiler = Compiler(string)
        actual = compiler.get_memory_bytes()

        # Assert
        assert actual == expected

    def test__get_memory_bytes__advanced_example_program_that_tests_all_opcodes__gets_expected_memory_bytes(self) -> None:
        # Arrange
        expected = MemoryBytesBuilder()\
            .msb('00').lsb('00').jmp()\
            .msb('00').lsb('01').data('FE')\
            .msb('00').lsb('02').data('00')\
            \
            .msb('01').lsb('00').data('37').comment('55')\
            .msb('01').lsb('01').data('14').comment('20')\
            .msb('01').lsb('02').data('02').comment(' 2')\
            .msb('01').lsb('03').data('01').comment(' 1')\
            \
            .msb('FE').lsb('00').load()\
            .msb('FE').lsb('01').data('01')\
            .msb('FE').lsb('02').data('00')\
            .msb('FE').lsb('03').add()\
            .msb('FE').lsb('04').data('01')\
            .msb('FE').lsb('05').data('02')\
            .msb('FE').lsb('06').store()\
            .msb('FE').lsb('07').data('01')\
            .msb('FE').lsb('08').data('00')\
            .msb('FE').lsb('09').load()\
            .msb('FE').lsb('0A').data('01')\
            .msb('FE').lsb('0B').data('01')\
            .msb('FE').lsb('0C').sub()\
            .msb('FE').lsb('0D').data('01')\
            .msb('FE').lsb('0E').data('03')\
            .msb('FE').lsb('0F').store()\
            .msb('FE').lsb('10').data('01')\
            .msb('FE').lsb('11').data('01')\
            .msb('FE').lsb('12').load()\
            .msb('FE').lsb('13').data('01')\
            .msb('FE').lsb('14').data('01')\
            .msb('FE').lsb('15').jz()\
            .msb('FE').lsb('16').data('FF')\
            .msb('FE').lsb('17').data('00')\
            .msb('FE').lsb('18').jmp()\
            .msb('FE').lsb('19').data('FE')\
            .msb('FE').lsb('1A').data('00')\
            \
            .msb('FF').lsb('00').load()\
            .msb('FF').lsb('01').data('01')\
            .msb('FF').lsb('02').data('00')\
            .msb('FF').lsb('03').store()\
            .msb('FF').lsb('04').data('FF')\
            .msb('FF').lsb('05').data('FF')\
            .msb('FF').lsb('06').halt()\
            .build()

        string = ''\
            + '00 00 JMP\n'\
            + '00 01 FE\n'\
            + '00 02 00\n'\
            + '\n'\
            + '01 00 37; 55\n'\
            + '01 01 14; 20\n'\
            + '01 02 02;  2\n'\
            + '01 03 01;  1\n'\
            + '\n'\
            + 'FE 00 LOAD\n'\
            + 'FE 01 01\n'\
            + 'FE 02 00\n'\
            + 'FE 03 ADD\n'\
            + 'FE 04 01\n'\
            + 'FE 05 02\n'\
            + 'FE 06 STORE\n'\
            + 'FE 07 01\n'\
            + 'FE 08 00\n'\
            + 'FE 09 LOAD\n'\
            + 'FE 0A 01\n'\
            + 'FE 0B 01\n'\
            + 'FE 0C SUB\n'\
            + 'FE 0D 01\n'\
            + 'FE 0E 03\n'\
            + 'FE 0F STORE\n'\
            + 'FE 10 01\n'\
            + 'FE 11 01\n'\
            + 'FE 12 LOAD\n'\
            + 'FE 13 01\n'\
            + 'FE 14 01\n'\
            + 'FE 15 JZ\n'\
            + 'FE 16 FF\n'\
            + 'FE 17 00\n'\
            + 'FE 18 JMP\n'\
            + 'FE 19 FE\n'\
            + 'FE 1A 00\n'\
            + '\n'\
            + 'FF 00 LOAD\n'\
            + 'FF 01 01\n'\
            + 'FF 02 00\n'\
            + 'FF 03 STORE\n'\
            + 'FF 04 FF\n'\
            + 'FF 05 FF\n'\
            + 'FF 06 HALT\n'

        # Act
        compiler = Compiler(string)
        actual = compiler.get_memory_bytes()

        # Assert
        assert actual == expected
