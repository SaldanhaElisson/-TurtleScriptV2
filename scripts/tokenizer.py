import re

from errors.Errors import LexicalError
from errors.error_messages import ErrorMessages
from structs.gramatics import Operators, Delimiters, Comment
from structs.lexer import Lexer
from structs.symbol_table import SymbolTable
from structs.token_factory import TokenTypeFactory
from structs.token_list import TokenListTable


class Tokenizer:
  def __init__(self, lexer: Lexer, token_list: TokenListTable,
      symbol_table: SymbolTable, token_factory: TokenTypeFactory):
    self._lexer = lexer
    self._token_list = token_list
    self._symbol_table = symbol_table
    self._token_factory = token_factory

  def read_file(self, path_file: str) -> list[tuple[str, int]]:
    lines = []
    with open(path_file, "r", encoding="utf-8") as file:
      for i, line in enumerate(file, start=1):
        lines.append((line, i))
    return lines

  def string_separator(self, line: list[tuple[str, int]]) -> list[tuple[str, int, int]]:
    fixed_separators = [
      Delimiters.COLON.lexeme,
      Delimiters.SEMICOLON.lexeme,
      Delimiters.COMMA.lexeme,
      Delimiters.LEFT_PAR.lexeme,
      Delimiters.RIGHT_PAR.lexeme,
    ]
    fixed_sep_pattern = ''.join(re.escape(c) for c in fixed_separators)

    multi_char_operators = [
      Operators.EQUAL.lexeme,
      Operators.NOT_EQUAL.lexeme,
      Operators.LESS_EQUAL.lexeme,
      Operators.GREATER_EQUAL.lexeme,
    ]
    multi_char_pattern = '|'.join(re.escape(op) for op in multi_char_operators)

    pattern = (
        rf'("(?:[^"\\]|\\.)*")'
        + r'|(//)'
        + rf'|({multi_char_pattern})'
        + r'|(\d+\.\d+)'
        + r'|(\w+)'
        + rf'|([{fixed_sep_pattern}])'
        + r'|([^\w\s])'
    )

    tokens = []
    for line_chars, line_number in line:
      for match in re.finditer(pattern, line_chars):
        token = match.group(0)
        pos = match.start()

        if token == Comment.COMMENT.lexeme:
          break

        tokens.append((token, pos, line_number))

    return tokens

  def analise_line(self, path_file: str) -> None:
    lines = self.read_file(path_file)
    lexemes = self.string_separator(lines)

    self.verified_balanced_delimiters(self.filter_list(lexemes))

    for lexeme, column, line_number in lexemes:
      if lexeme:
        try:
          token_code = self._lexer.analyze(lexeme, line_number,
                                           column)
          if token_code is None:
            symbol = self._symbol_table.get_by_lexeme(lexeme)
            if symbol is None:
              token_code = self._symbol_table.add_symbol(lexeme)
            else:
              token_code = symbol
          self._token_list.add_token(token_code, lexeme, line_number, column)
        except LexicalError as e:
          raise e

  def filter_list(self, lexemes: list[tuple[str, int, int]]) -> list[tuple[str, int, int]]:
    delimiters_set = {d.value[1] for d in Delimiters}
    return [item for item in lexemes if item[0] in delimiters_set]

  def verified_balanced_delimiters(self, delimiters: list[tuple[str, int, int]]):
    opened_delimiters = [Delimiters.START.value[1], Delimiters.LEFT_PAR.value[1]]
    closed_delimiters = {
      Delimiters.END.value[1]: Delimiters.START.value[1],
      Delimiters.RIGHT_PAR.value[1]: Delimiters.LEFT_PAR.value[1]
    }

    stack = []

    for d, column, line in delimiters:
      if d in opened_delimiters:
        stack.append((d, column, line))
      elif d in closed_delimiters:
        if not stack:
          raise LexicalError(ErrorMessages.DELIMITER_CLOSED_ERROR.value, line,
                             column, d)
        last_open = stack.pop()
        if closed_delimiters[d] != last_open[0]:
          raise LexicalError(ErrorMessages.DELIMITER_NOT_CLOSED_ERROR.value,
                             line,column, d)
    if stack:
        delimiter = stack[0]
        raise LexicalError(ErrorMessages.DELIMITER_OPENED_ERROR.value, delimiter[2],
                           delimiter[1], delimiter[0])
    return True