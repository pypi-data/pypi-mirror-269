from bytecore.byte_register import ByteRegister
from bytecore.byte import Byte


class Syntax:
    BYTES: set[str] = set()
    OPCODES = {
        'HALT': '00',
        'LOAD': '01',
        'STORE': '02',
        'ADD': '04',
        'SUB': '08',
        'JMP': '10',
        'JZ': '20',
    }
    OPCODE_BYTES = {
        '00': 'HALT',
        '01': 'LOAD',
        '02': 'STORE',
        '04': 'ADD',
        '08': 'SUB',
        '10': 'JMP',
        '20': 'JZ',
    }
    OPCODE_EXPECTED_EXTRA_BYTES = {
        'HALT': 0,
        'LOAD': 2,
        'STORE': 2,
        'ADD': 2,
        'SUB': 2,
        'JMP': 2,
        'JZ': 2,
    }
    VALID_HEX = set(['0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'])

    @staticmethod
    def _get_bytes() -> set[str]:
        byte_set: set[str] = set()

        byte_register = ByteRegister()
        byte_register.read_high()
        byte_register.write_high()

        for value in range(Byte.COUNT_VALUES):
            byte_register.set_bus(Byte(value))
            byte_set.add(byte_register.get_hex())

        return byte_set


Syntax.BYTES = Syntax._get_bytes()
