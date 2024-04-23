from bytecorecompiler.lexical_analysis import LexicalAnalysis
from bytecorecompiler.syntax_analysis import SyntaxAnalysis
from bytecorecompiler.semantic_analysis import SemanticAnalysis
from bytecorecompiler.syntax_tree import SyntaxTree


class Parser:
    def __init__(self, string: str) -> None:
        lexical_analysis = LexicalAnalysis()
        tokens = lexical_analysis.parse(string)

        syntax_analysis = SyntaxAnalysis()
        syntax_trees = syntax_analysis.parse(tokens)

        semantic_analysis = SemanticAnalysis()
        self._syntax_trees = semantic_analysis.parse(syntax_trees)

    @property
    def syntax_trees(self) -> list[SyntaxTree]:
        return self._syntax_trees
