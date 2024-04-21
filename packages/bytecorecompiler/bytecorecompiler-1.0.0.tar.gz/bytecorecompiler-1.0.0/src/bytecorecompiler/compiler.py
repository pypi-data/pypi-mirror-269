from bytecore.byte import Byte
from bytecore.memory import Memory
from bytecorecompiler.parser import Parser
from bytecorecompiler.exception import ByteCoreCompilerException


class Compiler:
    def __init__(self, string: str) -> None:
        parser = Parser(string)
        self._syntax_trees = parser.syntax_trees
        self._memory_bytes = self._convert_syntax_trees_to_memory_bytes()

    def _convert_syntax_trees_to_memory_bytes(self) -> list[Byte]:
        memory_bytes = Memory.get_default_memory_bytes()

        for syntax_tree in self._syntax_trees:
            memory_address = syntax_tree.get_memory_address()
            data = syntax_tree.get_data()

            if memory_address is None or data is None:
                raise ConvertException(
                    'Should not be missing these data.')

            memory_bytes[memory_address] = Byte(data)

        return memory_bytes

    def get_memory_bytes(self) -> list[Byte]:
        return self._memory_bytes


class ConvertException(ByteCoreCompilerException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
