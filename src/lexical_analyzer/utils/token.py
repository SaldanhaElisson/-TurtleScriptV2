class Token:
    def __init__(self, token_type: str, lexeme: str, line: int, column: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column