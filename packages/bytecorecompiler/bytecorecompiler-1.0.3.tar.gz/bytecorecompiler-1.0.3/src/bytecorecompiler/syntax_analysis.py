from bytecorecompiler.lexical_analysis import LexicalAnalysis
from bytecorecompiler.syntax_tree import SyntaxTree, InvalidNoneState, InvalidMsbLength, InvalidMsbByte, InvalidLsbLength, InvalidLsbByte, InvalidOpcode, InvalidData
from bytecorecompiler.exception import ByteCoreCompilerException
from collections import deque
from typing import Deque


class SyntaxAnalysis:
    MSB = 1
    LSB = 2
    OPCODE = 3
    DATA = 4

    def parse(self, tokens: list[str]) -> list[SyntaxTree]:
        self._check_that_either_zero_or_three_tokens_per_newline(tokens)
        syntax_trees = self._parse_syntax_tree(tokens)
        self._validate_syntax_trees(syntax_trees)

        return syntax_trees

    def _check_that_either_zero_or_three_tokens_per_newline(self, tokens: list[str]) -> None:
        linenumber = 1
        number_of_tokens = 0

        if len(tokens) == 0:
            raise WrongNumberOfTokens(linenumber)

        for token in tokens:
            if token == LexicalAnalysis.LINE_FEED:
                if not (number_of_tokens == 0 or number_of_tokens == 3):
                    raise WrongNumberOfTokens(linenumber)

                linenumber += 1
                number_of_tokens = 0
            else:
                number_of_tokens += 1

        if not (number_of_tokens == 0 or number_of_tokens == 3):
            raise WrongNumberOfTokens(linenumber)

    def _parse_syntax_tree(self, tokens: list[str]) -> list[SyntaxTree]:
        syntax_trees: list[SyntaxTree] = []
        queue: Deque[str] = deque()
        linenumber = 1

        for token in tokens:
            if token == LexicalAnalysis.LINE_FEED:
                if len(queue) == 0:
                    syntax_trees.append(SyntaxTree(
                        None, None, None, linenumber))
                else:
                    msb = queue.popleft()
                    lsb = queue.popleft()
                    opcode = queue.popleft()
                    syntax_trees.append(SyntaxTree(
                        msb, lsb, opcode, linenumber))

                linenumber += 1
            else:
                queue.append(token)

        return syntax_trees

    def _validate_syntax_trees(self, syntax_trees: list[SyntaxTree]) -> None:
        for index, syntax_tree in enumerate(syntax_trees):
            line_number = index + 1

            try:
                syntax_tree.validate()
            except InvalidNoneState:
                raise InternalSyntaxError(line_number)
            except InvalidMsbLength:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.MSB, 'Invalid MSB length')
            except InvalidMsbByte:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.MSB, 'Invalid MSB byte')
            except InvalidLsbLength:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.LSB, 'Invalid LSB length')
            except InvalidLsbByte:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.LSB, 'Invalid LSB length')
            except InvalidOpcode:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.OPCODE, 'Invalid OPCODE')
            except InvalidData:
                raise SyntaxAnalysisError(
                    line_number, SyntaxAnalysis.DATA, 'Invalid DATA')
            except Exception:
                raise InternalSyntaxError(line_number)


class SyntaxAnalysisException(ByteCoreCompilerException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class WrongNumberOfTokens(SyntaxAnalysisException):
    def __init__(self, line_number: int) -> None:
        self.message = f'Wrong number of tokens on line: {line_number}.'

        super().__init__(self.message)


class InternalSyntaxError(SyntaxAnalysisException):
    def __init__(self, line_number: int) -> None:
        self.message = f'Internal syntax error on line: {line_number}.'

        super().__init__(self.message)


class SyntaxAnalysisError(SyntaxAnalysisException):
    def __init__(self, line_number: int, token_number: int, message: str) -> None:
        subject = ''

        if token_number == SyntaxAnalysis.MSB:
            subject = 'MSB'
        elif token_number == SyntaxAnalysis.LSB:
            subject = 'LSB'
        elif token_number == SyntaxAnalysis.OPCODE:
            subject = 'OPCODE'
        elif token_number == SyntaxAnalysis.DATA:
            subject = 'DATA'
        else:
            raise InternalSyntaxError(line_number)

        self.message = f'Syntax error: {message} on line: {line_number}.'

        super().__init__(self.message)
