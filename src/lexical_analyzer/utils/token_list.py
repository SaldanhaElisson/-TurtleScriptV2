from errors.error_messages import ErrorMessages
from errors.error import LexicalError
from .token_class import KeyWords
from .token_factory import TokenTypeFactory


class TokenListTable:
    def __init__(self, token_factory: TokenTypeFactory) -> None:
        self._token_list: list[dict] = []
        self._token_factory = token_factory

    @property
    def token_list(self) -> list[dict]:
        return self._token_list

    @property
    def token_factory(self) -> TokenTypeFactory:
        return self._token_factory

    def add_token(self, ref_type: int, lexeme: str, line: int, column: int) -> None:
        token_type = self.token_factory.factory(ref_type)

        if token_type == KeyWords.FLOAT.name and lexeme != KeyWords.FLOAT.value[1]:
            lexeme = float(lexeme)
        elif (
            token_type == KeyWords.INTEGER.name and lexeme != KeyWords.INTEGER.value[1]
        ):
            lexeme = int(lexeme)

        if token_type is None:
            raise LexicalError(ErrorMessages.UNKNOWN_SYMBOL.value, line, column, lexeme)

        token = {
            "lexeme": lexeme,
            "type": token_type,
            "ref_type": ref_type,
            "line": line,
            "column": column,
        }
        self.token_list.append(token)

    def get_tokens(self) -> list[dict]:
        return self.token_list
