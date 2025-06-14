from .token_class import Comment


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: list[tuple[int, dict]] = []
        self._ref_symbol = Comment.COMMENT.value[0]

    def add_symbol(self, lexeme: str) -> int:
        self._ref_symbol += 1
        symbol = {
            "type": "ID",
            "lexeme": lexeme,
        }
        self._symbols.append((self._ref_symbol, symbol))
        return self._ref_symbol

    def get_by_code(self, symbol_ref: int) -> str | None:
        for ref, symbol in self._symbols:
            if ref == symbol_ref:
                return symbol["type"]
        return None

    def get_by_lexeme(self, lexeme: str) -> int | None:
        for ref, symbol in self._symbols:
            if symbol["lexeme"] == lexeme:
                return ref
        return None

    def get_symbols(self) -> list[tuple[int, dict]]:
        return self._symbols
