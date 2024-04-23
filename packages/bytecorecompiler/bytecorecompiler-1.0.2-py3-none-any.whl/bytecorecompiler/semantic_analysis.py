from bytecorecompiler.syntax_tree import SyntaxTree
from bytecorecompiler.syntax import Syntax
from bytecorecompiler.exception import ByteCoreCompilerException


class SemanticAnalysis:
    def parse(self, syntax_trees: list[SyntaxTree]) -> list[SyntaxTree]:
        self._syntax_trees: dict[int, SyntaxTree] = {}
        self._check_if_duplicate_memory_address(syntax_trees)
        self._check_if_opcodes_has_expected_extra_bytes()
        self._filter_away_empty_syntax_trees()

        return list(self._syntax_trees.values())

    def _check_if_duplicate_memory_address(self, syntax_trees: list[SyntaxTree]) -> None:
        for syntax_tree in syntax_trees:
            address = syntax_tree.get_memory_address()

            if address is None:
                continue

            if address in self._syntax_trees:
                raise DuplicateMemoryAddressAssignment(syntax_tree.linenumber)

            self._syntax_trees[address] = syntax_tree

    def _check_if_opcodes_has_expected_extra_bytes(self) -> None:
        for key in sorted(self._syntax_trees):
            syntax_tree = self._syntax_trees[key]

            if not syntax_tree.is_opcode:
                continue

            if syntax_tree.data is None:
                continue

            opcode = Syntax.OPCODE_BYTES[syntax_tree.data]
            expected_extra_bytes = Syntax.OPCODE_EXPECTED_EXTRA_BYTES[opcode]

            for i in range(1, expected_extra_bytes + 1):
                sub_key = key + i

                if sub_key not in self._syntax_trees:
                    raise MissingExtendedMemoryAddress(syntax_tree.linenumber)

                if self._syntax_trees[sub_key].is_opcode:
                    raise MissingExtendedMemoryAddress(syntax_tree.linenumber)

    def _filter_away_empty_syntax_trees(self) -> None:
        self._syntax_trees = {
            key: syntax_tree for key, syntax_tree in self._syntax_trees.items() if not syntax_tree.is_all_empty}


class SemanticAnalysisException(ByteCoreCompilerException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DuplicateMemoryAddressAssignment(SemanticAnalysisException):
    def __init__(self, line_number: int | None) -> None:
        formatted_line_number = 'None'

        if line_number is not None:
            formatted_line_number = str(line_number)

        self.message = f'Memory address has already been assigned to on line: {formatted_line_number}.'

        super().__init__(self.message)


class MissingExtendedMemoryAddress(SemanticAnalysisException):
    def __init__(self, line_number: int | None) -> None:
        formatted_line_number = 'None'

        if line_number is not None:
            formatted_line_number = str(line_number)

        self.message = f'Missing extended memory address after OPCODE on line: {formatted_line_number}.'

        super().__init__(self.message)
