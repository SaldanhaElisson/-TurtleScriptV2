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
  REPEAT = (13, "repita")
  END_REPEAT = (14, "fim_repita")
  TIMES = (15, "vezes")

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
  START = (16, "inicio")
  END = (17, "fim")
  COLON = (18, ":")
  SEMICOLON = (19, ";")
  QUOTATION_MARK = (20, '"')
  COMMA = (21, ',')
  LEFT_PAR = (22, '(')
  RIGHT_PAR = (23, ')')
  SINGLE_QUOTE = (24, '\'')
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
  EQUAL = (25, "==")
  NOT_EQUAL = (26, "!=")
  LESS_THAN = (27, "<")
  LESS_EQUAL = (28, "<=")
  GREATER_THAN = (29, ">")
  GREATER_EQUAL = (30, ">=")
  PLUS = (31, "+")
  MINUS = (32, "-")
  MULTIPLICATION = (33, "*")
  DIVISIVE = (34, "/")
  ASSIGN = (35, "=")
  PERCENTAGE = (36, "%")

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
  COMMENT = (37, "//")

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