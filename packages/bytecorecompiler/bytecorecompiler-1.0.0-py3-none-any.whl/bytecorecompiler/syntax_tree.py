from bytecorecompiler.syntax import Syntax
from bytecorecompiler.exception import ByteCoreCompilerException


class SyntaxTree:
    def __init__(self, msb: str | None, lsb: str | None, data: str | None, linenumber: int | None) -> None:
        self._msb = None
        if msb is not None:
            self._msb = msb.upper()

        self._lsb = None
        if lsb is not None:
            self._lsb = lsb.upper()

        self._data = None
        if data is not None:
            self._data = data.upper()

        self._linenumber = linenumber
        self._is_all_empty = self._msb is None and self._lsb is None and self._data is None
        self._is_opcode = False
        self._has_validated = False

    @property
    def msb(self) -> str | None:
        return self._msb

    @property
    def lsb(self) -> str | None:
        return self._lsb

    @property
    def data(self) -> str | None:
        return self._data

    @property
    def linenumber(self) -> int | None:
        return self._linenumber

    @property
    def has_validated(self) -> bool:
        return self._has_validated

    @property
    def is_opcode(self) -> bool:
        return self._is_opcode

    @property
    def is_all_empty(self) -> bool:
        return self._is_all_empty

    def validate(self) -> None:
        if self.has_validated:
            return

        if self.is_all_empty:
            self._has_validated = True
            return

        if self.msb is None or self.lsb is None or self.data is None:
            raise InvalidNoneState

        self._validate_msb_length(self.msb)
        self._validate_msb_byte(self.msb)

        self._validate_lsb_length(self.lsb)
        self._validate_lsb_byte(self.lsb)

        self._validate_data()

        self._has_validated = True

    def _validate_msb_length(self, msb: str) -> None:
        if len(msb) != 2:
            raise InvalidMsbLength

    def _validate_lsb_length(self, lsb: str) -> None:
        if len(lsb) != 2:
            raise InvalidLsbLength

    def _validate_msb_byte(self, msb: str) -> None:
        if msb not in Syntax.BYTES:
            raise InvalidMsbByte

    def _validate_lsb_byte(self, lsb: str) -> None:
        if lsb not in Syntax.BYTES:
            raise InvalidLsbByte

    def _validate_data(self) -> None:
        if self._is_data():
            return

        if self.data is not None and self.data not in Syntax.OPCODES and len(self.data) == 2:
            raise InvalidData

        if self.is_opcode_keyword():
            self._is_opcode = True

            if self._data is not None:
                self._data = Syntax.OPCODES[self._data]

            return

        raise InvalidOpcode

    def is_opcode_keyword(self) -> bool:
        if self.data is None:
            return False

        return self.data in Syntax.OPCODES

    def _is_data(self) -> bool:
        if self.data is None:
            return False

        if len(self.data) != 2:
            return False

        return self.data[0] in Syntax.VALID_HEX and self.data[1] in Syntax.VALID_HEX

    def get_memory_address(self) -> int | None:
        if self.msb is None or self.lsb is None:
            return None

        return int(self.msb + self.lsb, 16)

    def get_data(self) -> int | None:
        if self.data is None:
            return None

        return int(self.data, 16)


class SyntaxTreeException(ByteCoreCompilerException):
    def __init__(self) -> None:
        self.message = 'Syntax Tree Exception'
        super().__init__(self.message)


class InvalidNoneState(SyntaxTreeException):
    pass


class InvalidMsbLength(SyntaxTreeException):
    pass


class InvalidLsbLength(SyntaxTreeException):
    pass


class InvalidMsbByte(SyntaxTreeException):
    pass


class InvalidLsbByte(SyntaxTreeException):
    pass


class InvalidOpcode(SyntaxTreeException):
    pass


class InvalidData(SyntaxTreeException):
    pass
