from bytecorecompiler.compiler import Compiler
from bytecore.emulator import ByteCore
from bytecore.byte import Byte


class TestExamples:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__get_memory_bytes__simple_example_program__halts_and_last_memory_location_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(50)
        bytecore_assembly = """
00 00 LOAD
00 01 00
00 02 0A
00 03 ADD
00 04 00
00 05 0B
00 06 STORE
00 07 FF
00 08 FF
00 09 HALT
00 0A 14; 20
00 0B 1E; 30
"""

        # Act
        memory_bytes = Compiler(bytecore_assembly).get_memory_bytes()
        byte_core = ByteCore(memory_bytes)
        byte_core.cycle_until_halt()
        dump = byte_core.dump()
        actual = dump.memory[-1]  # equals 50

        # Assert
        assert actual == expected

    def test__get_memory_bytes__advanced_example_program_that_tests_all_opcodes__halts_and_last_memory_location_contains_expected_value(self) -> None:
        # Arrange
        expected = Byte(95)
        bytecore_assembly = """
00 00 JMP
00 01 FE
00 02 00

01 00 37; 55
01 01 14; 20
01 02 02;  2
01 03 01;  1

FE 00 LOAD
FE 01 01
FE 02 00
FE 03 ADD
FE 04 01
FE 05 02
FE 06 STORE
FE 07 01
FE 08 00
FE 09 LOAD
FE 0A 01
FE 0B 01
FE 0C SUB
FE 0D 01
FE 0E 03
FE 0F STORE
FE 10 01
FE 11 01
FE 12 LOAD
FE 13 01
FE 14 01
FE 15 JZ
FE 16 FF
FE 17 00
FE 18 JMP
FE 19 FE
FE 1A 00

FF 00 LOAD
FF 01 01
FF 02 00
FF 03 STORE
FF 04 FF
FF 05 FF
FF 06 HALT
"""

        # Act
        memory_bytes = Compiler(bytecore_assembly).get_memory_bytes()
        byte_core = ByteCore(memory_bytes)
        byte_core.cycle_until_halt()
        dump = byte_core.dump()
        actual = dump.memory[-1]  # equals 95

        # Assert
        assert actual == expected
