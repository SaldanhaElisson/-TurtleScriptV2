from .error_types import ErrorType


class GenericError(Exception):
    def __init__(
        self,
        error_type: ErrorType,
        message: str,
        line: int,
        column: int,
        symbol: object,
    ) -> None:
        self._error_type = error_type
        self._message = message
        self._line = line
        self._column = column
        self._symbol = symbol
        super().__init__(self.__str__())

    @property
    def error_type(self) -> ErrorType:
        return self._error_type

    @property
    def message(self) -> str:
        return self._message

    @property
    def line(self) -> int:
        return self._line

    @property
    def column(self) -> int:
        return self._column

    @property
    def symbol(self) -> object:
        return self._symbol

    def __str__(self) -> str:
        location = (
            f" (line {self.line}, column {self.column})"
            if self.line is not None
            else ""
        )
        return f"[Error {self.error_type}]{location} | symbol - ' {self.symbol} ': {self.message}"


class LexicalError(GenericError):
    def __init__(self, message: str, line: int, column: int, symbol: object) -> None:
        super().__init__(ErrorType.LEXICAL, message, line, column, symbol)


class SyntacticError(GenericError):
    def __init__(self, message: str, line: int, column: int, symbol: object) -> None:
        super().__init__(ErrorType.SYNTACTIC, message, line, column, symbol)


class SemanticError(GenericError):
    def __init__(self, message: str, line: int, column: int, symbol: object) -> None:
        super().__init__(ErrorType.SEMANTIC, message, line, column, symbol)