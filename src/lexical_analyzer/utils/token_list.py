from src.errors.error_messages import ErrorMessages
from src.errors.error import LexicalError
from .token import Token
from .token_class import KeyWords
from .token_factory import TokenTypeFactory


class TokenListTable:
    def __init__(self, token_factory: TokenTypeFactory) -> None:
        self._token_list: list[Token] = []
        self._token_factory = token_factory

    @property
    def token_list(self) -> list[Token]:
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
            token_type = "IDENTIFIER"

        token = Token(token_type, lexeme, line, column)

        self.token_list.append(token)

    def get_tokens(self) -> list[Token]:
        return self.token_list
