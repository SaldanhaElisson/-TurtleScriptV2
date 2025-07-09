from .token_class import KeyWords, Operators, Comment, Delimiters
from .symbol_table import SymbolTable


class TokenTypeFactory:
    def __init__(self, symbol_table: SymbolTable) -> None:
        self.symbol_table = symbol_table

    def factory(self, code: int) -> str | None:
        if 1 <= code <= 15:
            return KeyWords.get_by_code(code)
        elif 16 <= code <= 24:
            return Delimiters.get_by_code(code)
        elif 25 <= code <= 36:
            return Operators.get_by_code(code)
        elif code == 37:
            return Comment.get_by_code(code)
        elif code >= 36:
            return self.symbol_table.get_by_code_with_value(code)
        else:
            return None
