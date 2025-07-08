from structs.gramatics import KeyWords, Operators, Comment, Delimiters
from structs.symbol_table import SymbolTable


class TokenTypeFactory:
  def __init__(self, symbol_table: SymbolTable) -> None:
    self.symbol_table = symbol_table

  def factory(self, code: int) -> str | None:
    if 1 <= code <= 12:
      return KeyWords.get_by_code(code)
    elif 13 <= code <= 21:
      return Delimiters.get_by_code(code)
    elif 22 <= code <= 33:
      return Operators.get_by_code(code)
    elif code == Comment.COMMENT.value[0]:
      return Comment.get_by_code(code)
    elif code > Comment.COMMENT.value[0]:
      return self.symbol_table.get_by_code(code)
    else:
      return None
