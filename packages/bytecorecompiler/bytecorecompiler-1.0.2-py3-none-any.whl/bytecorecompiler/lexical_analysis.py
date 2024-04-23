
class LexicalAnalysis:
    LINE_FEED = '\n'
    CARRIAGE_RETURN = '\r'
    CARRIAGE_RETURN_LINE_FEED = '\r\n'
    COMMENT_SEPARATOR = ';'
    SPACE = ' '

    def parse(self, string: str) -> list[str]:
        string = self._replace_newlines(string)
        tokens = self._split_lines(string)

        if len(tokens) == 0:
            tokens.append(LexicalAnalysis.LINE_FEED)

        if tokens[-1][-1] != LexicalAnalysis.LINE_FEED:
            token = tokens[-1]
            token += LexicalAnalysis.LINE_FEED
            tokens[-1] = token

        tokens = self._remove_comments(tokens)
        tokens = self._split_newlines_tokens(tokens)
        tokens = self._split_lines_on_space(tokens)
        tokens = self._remove_empty_tokens(tokens)

        return tokens

    def _replace_newlines(self, string: str) -> str:
        while True:
            temp = string
            string = string.replace(
                LexicalAnalysis.CARRIAGE_RETURN, LexicalAnalysis.LINE_FEED)

            if temp == string:
                break

        while True:
            temp = string
            string = string.replace(
                LexicalAnalysis.CARRIAGE_RETURN_LINE_FEED, LexicalAnalysis.LINE_FEED)

            if temp == string:
                break

        return string

    def _split_lines(self, string: str) -> list[str]:
        return string.splitlines(keepends=True)

    def _remove_comments(self, tokens: list[str]) -> list[str]:
        modified_tokens: list[str] = []

        for token in tokens:
            temp = ''
            did_break = False

            for c in token:
                if c == LexicalAnalysis.COMMENT_SEPARATOR:
                    did_break = True
                    break

                temp += c

            if did_break and token[-1] == LexicalAnalysis.LINE_FEED:
                temp += LexicalAnalysis.LINE_FEED

            modified_tokens.append(temp)

        return modified_tokens

    def _split_newlines_tokens(self, tokens: list[str]) -> list[str]:
        output_tokens: list[str] = []

        for token in tokens:
            found_newline = False

            if token[-1] == LexicalAnalysis.LINE_FEED:
                found_newline = True
                token = token[:-1]

            if len(token) > 0:
                output_tokens.append(token)

            if found_newline:
                output_tokens.append(LexicalAnalysis.LINE_FEED)

        return output_tokens

    def _split_lines_on_space(self, tokens: list[str]) -> list[str]:
        output_tokens: list[str] = []

        for token in tokens:
            splitted_tokens = token.split(sep=LexicalAnalysis.SPACE)
            output_tokens += splitted_tokens

        return output_tokens

    def _remove_empty_tokens(self, tokens: list[str]) -> list[str]:
        output_tokens: list[str] = []

        for token in tokens:
            if len(token) == 0:
                continue

            output_tokens.append(token)

        return output_tokens
