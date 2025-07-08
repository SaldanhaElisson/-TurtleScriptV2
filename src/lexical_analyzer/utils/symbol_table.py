from .token_class import Comment


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: list[dict] = []
        self._ref_symbol = Comment.COMMENT.value[0]

    def add_symbol(self, lexeme: str, type: str) -> int:
        self._ref_symbol += 1
        symbol = {
            "type": type,
            "value": "IDENTIFIER",
            "lexeme": lexeme,
            "code": self._ref_symbol,
        }
        self._symbols.append(symbol)
        return self._ref_symbol

    def get_by_code(self, symbol_ref: int) -> str | None:
        for symbol in self._symbols:
            if symbol["code"] == symbol_ref:
                return symbol["type"]
        return None

    def get_by_code_lexeme(self, lexeme: str) -> int | None:
        for symbol in self._symbols:
            if symbol["lexeme"] == lexeme:
                return symbol["code"]
        return None

    def get_by_lexeme(self, lexeme: str) -> str | None:
        for symbol in self._symbols:
            if symbol["lexeme"] == lexeme:
                return symbol["type"]
        return None

    def get_symbols(self) -> list[dict]:
        return self._symbols
