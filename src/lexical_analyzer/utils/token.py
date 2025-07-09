class Token:
    def __init__(self, token_type: str, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token(type='{self.token_type}', lexeme='{self.lexeme}', line={self.line}, column={self.column})"