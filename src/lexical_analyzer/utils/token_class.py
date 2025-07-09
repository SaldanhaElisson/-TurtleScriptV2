from enum import Enum

class KeyWords(Enum):
  INTEGER = (1, "inteiro")
  TEXT = (2, "texto")
  BOOLEAN = (3, "logico")
  FLOAT = (4, "real")
  VAR = (5, "var")
  IF = (6, "se")
  THEN = (7, "entao")
  END_IF = (8, "fim_se")
  ELSE = (9, "senao")
  WHILE = (10, "enquanto")
  DO = (11, "faca")
  END_WHILE = (12, "fim_enquanto")

  def __init__(self, code: int, lexeme: str):
    self._code = code
    self._lexeme = lexeme

  @property
  def code(self) -> int:
      return self._code

  @property
  def lexeme(self):
      return self._lexeme

  @classmethod
  def get_by_code(cls, code: int) -> str | None:
    for item in cls:
      if item.code == code:
        return item.name
    return None

class Delimiters(Enum):
  START = (13, "inicio")
  END = (14, "fim")
  COLON = (15, ":")
  SEMICOLON = (16, ";")
  QUOTATION_MARK = (17, '"')
  COMMA = (18, ',')
  LEFT_PAR = (19, '(')
  RIGHT_PAR = (20, ')')
  SINGLE_QUOTE = (21, '\'')
  def __init__(self, code: int, lexeme: str):
    self._code = code
    self._lexeme = lexeme

  @property
  def code(self):
    return self._code

  @property
  def lexeme(self):
    return self._lexeme

  @classmethod
  def get_by_code(cls, code: int) -> str | None:
    for item in cls:
      if item.code == code:
        return item.name
    return None


class Operators(Enum):
  EQUAL = (22, "==")
  NOT_EQUAL = (23, "!=")
  LESS_THAN = (24, "<")
  LESS_EQUAL = (25, "<=")
  GREATER_THAN = (26, ">")
  GREATER_EQUAL = (27, ">=")
  PLUS = (28, "+")
  MINUS = (29, "-")
  MULTIPLICATION = (30, "*")
  DIVISIVE = (31, "/")
  ASSIGN = (32, "=")
  PERCENTAGE = (33, "%")

  def __init__(self, code: int, lexeme: str):
    self._code = code
    self._lexeme = lexeme

  @property
  def code(self):
    return self._code

  @property
  def lexeme(self):
    return self._lexeme

  @classmethod
  def get_by_code(cls, code: int) -> str | None:
    for item in cls:
      if item.code == code:
        return item.name
    return None


class Comment(Enum):
  COMMENT = (34, "//")

  def __init__(self, code: int, lexeme: str):
    self._code = code
    self._lexeme = lexeme

  @property
  def code(self):
    return self._code

  @property
  def lexeme(self):
    return self._lexeme

  @classmethod
  def get_by_code(cls, code: int) -> str | None:
    for item in cls:
      if item.code == code:
        return item.name
    return None