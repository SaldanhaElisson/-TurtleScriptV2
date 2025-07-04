import re

from src.errors.error import LexicalError
from src.errors.error_messages import ErrorMessages
from .token_class import Comment, KeyWords, Delimiters, Operators


class Lexer:
    def __init__(self):
        self.token_specs = [
            ("KEYWORD", f"\\b({'|'.join(re.escape(e.lexeme) for e in KeyWords)})\\b"),
            ("DELIMITER", f"{'|'.join(re.escape(e.lexeme) for e in Delimiters)}"),
            (
                "OPERATOR",
                f"{'|'.join(sorted((re.escape(e.lexeme) for e in Operators), key=len, reverse=True))}",
            ),
            ("BOOLEAN", r"\b(verdadeiro|falso)\b"),
            ("FLOAT", r"\d+\.\d+"),
            ("INTEGER", r"\d+"),
            ("TEXT", r'"[^"\n]*"'),
            ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ]

        self.regex = re.compile(
            "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_specs)
        )

    @staticmethod
    def verify_error_id_not_match(self, lexeme: str, line: int, column: int) -> None:
        if re.match(r"[^a-zA-Z0-9_\s\"'()\[\]{}\.,;:+\-*/%=<>!&|^~?]", lexeme):
            raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)

        if re.match(r"^[^a-zA-Z_]", lexeme):
            raise LexicalError(ErrorMessages.FIRST_SYMBOL.value, line, column, lexeme)

        raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)

    def analyze(self, lexeme: str, line: int, column: int) -> int | None | str:
        match = self.regex.fullmatch(lexeme)
        if not match:
            return self.verify_error_id_not_match(self, lexeme, line, column)

        token_type = match.lastgroup

        if token_type == "DELIMITER" and lexeme == '"' or lexeme == "'":
            raise LexicalError(
                ErrorMessages.TEXT_OR_CHAR_NOT_CLOSED.value, line, column, lexeme
            )

        if token_type == "INTEGER":
            return KeyWords.INTEGER.code

        if token_type == "FLOAT":
            return KeyWords.FLOAT.code

        if token_type == "TEXT":
            return KeyWords.TEXT.code

        if token_type == "BOOLEAN" and lexeme in ["verdadeiro", "falso"]:
            return KeyWords.BOOLEAN.code
        if token_type == "ID":
            return None

        code = self.get_code_by_token(token_type, lexeme, line, column)
        if code is None:
            raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)
        return code

    @staticmethod
    def get_code_by_token(
        token_type: str, lexeme: str, line: int, column: int
    ) -> int | None:
        enum_map = {
            "KEYWORD": KeyWords,
            "DELIMITER": Delimiters,
            "OPERATOR": Operators,
            "COMMENT": Comment,
        }

        enum_class = enum_map.get(token_type)
        if enum_class is None:
            raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)

        for item in enum_class:
            if item.lexeme == lexeme:
                return item.code
        raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)
