from unittest.mock import MagicMock

import pytest

<<<<<<< HEAD
from errors.Errors import LexicalError
from scripts.tokenizer import Tokenizer
from structs.lexer import Lexer
from structs.symbol_table import SymbolTable
from structs.token_factory import TokenTypeFactory
from structs.token_list import TokenListTable


class TestLexicalTokenizer:
  def setup_method(self, method):
    self.symbol_table = SymbolTable()
    self.token_type_factory = TokenTypeFactory(self.symbol_table)
    self.token_list_table = TokenListTable(self.token_type_factory)
    self.lexer = Lexer()
    self.tokenizer_obj = Tokenizer(self.lexer, self.token_list_table, self.symbol_table,
                              self.token_type_factory)
    self.expectative_line_division_operator = [
      ('(', 0, 1), ('a', 1, 1), ('==', 3, 1), ('b', 6, 1), ('!=', 8, 1), ('c', 11, 1),
      (')', 12, 1), ('(', 14, 1), ('g', 15, 1), ('<=', 17, 1), ('d', 20, 1), ('>=', 22, 1)
      , ('e', 25, 1), (')', 26, 1)
    ]
    self.expectative_line_division_float = [
      ("angulo", 0, 1), ('=', 7, 1), ('144.0', 9, 1), (';', 14, 1)
    ]
    self.expectative_line_multiple_delimiters = [
      ("var", 0, 1), ("inteiro", 4, 1), (":", 12, 1),("lado", 14, 1),
      (",", 19, 1), ("altura", 21, 1), (";", 28, 1)
    ]
    self.expectative_line_comment = []
    self.expectative_line_condition = [
      ("(", 0, 1), ("se", 1, 1),("(", 3, 1),("lado", 4, 1),("%", 9, 1),
      ("2", 11, 1),(")", 12, 1),("==", 14, 1),("0", 17, 1),(")", 18, 1)
    ]
    self.expectative_string_separator1 = [
      ('inicio', 0, 1), ('avancar', 2, 3), ('150', 10, 3),
      (';', 13, 3), ('girar_direita', 2, 4), ('90', 16, 4), (';', 18, 4),
      ('avancar', 2, 6), ('150', 10, 6), (';', 13, 6), ('girar_direita', 2, 7),
      ('90', 16, 7), (';', 18, 7), ('avancar', 2, 9), ('150', 10, 9), (';', 13, 9),
      ('girar_direita', 2, 10), ('90', 16, 10), (';', 18, 10), ('avancar', 2, 12),
      ('150', 10, 12), (';', 13, 12), ('girar_direita', 2, 13), ('90', 16, 13),
      (';', 18, 13), ('fim', 0, 14)]
    self.expectative_read_file1 = [
      ('inicio', 1), ('  // Desenha as quatro arestas do quadrado', 2),
      ('  avancar 150;', 3), ('  girar_direita 90;', 4), ('', 5), ('  avancar 150;', 6),
      ('  girar_direita 90;', 7), ('', 8), ('  avancar 150;', 9), ('  girar_direita 90;', 10),
      ('', 11), ('  avancar 150;', 12), ('  girar_direita 90;', 13), ('fim', 14)]
    self.expectative_string_separator2 = [
      ('val@doção', 0, 1)]
    self.expectative_read_file2 = [
      ('val@doção', 1)]
    self.expectative_string_separator3 = [
      ('1test', 0, 1)]
    self.expectative_read_file3 = [
      ('1test', 1)]
    self.expectative_string_separator4 = [
      ('"', 0, 1), ('1test', 1, 1)]
    self.expectative_read_file4 = [
      ('"1test', 1)]
    self.expectative_string_separator5 = [('(', 0, 1), ('(', 1, 1), (')', 2, 1)]
    self.expectative_read_file5 = [
      ([('(()', 1)])]
    self.expectative_string_separator6 = [('(', 0, 1), (')', 1, 1), (')', 2, 1)]
    self.expectative_read_file5 = [
      ([('())', 1)])]

  @pytest.mark.parametrize("line", [[("(a == b != c) (g <= d >= e)", 1)]])
  def test_operators_with_string_separator(self, line: list[tuple[str, int]]):
    token_list = self.tokenizer_obj.string_separator(line)

    assert token_list[0] == self.expectative_line_division_operator[0]
    assert token_list[1] == self.expectative_line_division_operator[1]
    assert token_list[2] == self.expectative_line_division_operator[2]
    assert token_list[3] == self.expectative_line_division_operator[3]
    assert token_list[4] == self.expectative_line_division_operator[4]
    assert token_list[5] == self.expectative_line_division_operator[5]
    assert token_list[6] == self.expectative_line_division_operator[6]
    assert token_list[7] == self.expectative_line_division_operator[7]
    assert token_list[8] == self.expectative_line_division_operator[8]
    assert token_list[9] == self.expectative_line_division_operator[9]
    assert token_list[10] == self.expectative_line_division_operator[10]
    assert token_list[11] == self.expectative_line_division_operator[11]

  @pytest.mark.parametrize("line", [[("angulo = 144.0;", 1)]])
  def test_float_with_string_separator(self, line: list[tuple[str, int]]):
    token_list = self.tokenizer_obj.string_separator(line)

    assert token_list[0] == self.expectative_line_division_float[0]
    assert token_list[1] == self.expectative_line_division_float[1]
    assert token_list[2] == self.expectative_line_division_float[2]
    assert token_list[3] == self.expectative_line_division_float[3]

  @pytest.mark.parametrize("line", [[("var inteiro : lado , altura ;", 1)]])
  def test_multiple_delimiter_with_string_separator(self, line: list[tuple[str, int]]):
    token_list = self.tokenizer_obj.string_separator(line)

    assert token_list[0] == self.expectative_line_multiple_delimiters[0]
    assert token_list[1] == self.expectative_line_multiple_delimiters[1]
    assert token_list[2] == self.expectative_line_multiple_delimiters[2]
    assert token_list[3] == self.expectative_line_multiple_delimiters[3]
    assert token_list[4] == self.expectative_line_multiple_delimiters[4]
    assert token_list[5] == self.expectative_line_multiple_delimiters[5]
    assert token_list[6] == self.expectative_line_multiple_delimiters[6]

  @pytest.mark.parametrize("line", [[("// simplesmente um comentário", 1)]])
  def test_multiple_delimiter_with_string_separator(self, line: list[tuple[str, int]]):
    token_list = self.tokenizer_obj.string_separator(line)

    assert token_list == self.expectative_line_comment

  @pytest.mark.parametrize("line", [[("(se(lado % 2) == 0)", 1)]])
  def test_par_with_string_separator(self, line: list[tuple[str, int]]):
    token_list = self.tokenizer_obj.string_separator(line)

    assert token_list[0] == self.expectative_line_condition[0]
    assert token_list[1] == self.expectative_line_condition[1]
    assert token_list[2] == self.expectative_line_condition[2]
    assert token_list[3] == self.expectative_line_condition[3]
    assert token_list[4] == self.expectative_line_condition[4]
    assert token_list[5] == self.expectative_line_condition[5]
    assert token_list[6] == self.expectative_line_condition[6]
    assert token_list[7] == self.expectative_line_condition[7]
    assert token_list[8] == self.expectative_line_condition[8]
    assert token_list[9] == self.expectative_line_condition[9]

  @pytest.mark.parametrize("line", ["inputs/entrada1.txt"])
  def test_list_token_and_symbols_with_analise_line(self,line: str):
    self.tokenizer_obj.read_file = MagicMock(return_value=self.expectative_read_file1)
    self.tokenizer_obj.string_separator = MagicMock(return_value=self.expectative_string_separator1)

    isNone = self.tokenizer_obj.analise_line(line)

    assert isNone is None

  @pytest.mark.parametrize("line", ["inputs/char_invalido.txt"])
  def test_unknown_symbol_error_with_analise_line(self, line: str):
    self.tokenizer_obj.read_file = MagicMock(
      return_value=self.expectative_read_file2)
    self.tokenizer_obj.string_separator = MagicMock(
      return_value=self.expectative_string_separator2)

    regex = r"\[Error ErrorType\.LEXICAL\]( \(line \d+, column \d+\))? \| symbol - ' .*? ': Symbol not known to the compiler, "
    with pytest.raises(LexicalError, match=regex):
      self.tokenizer_obj.analise_line(line)

  @pytest.mark.parametrize("line", ["inputs/first_char_is_number_on_id.txt"])
  def test_first_symbol_is_number_error_with_analise_line(self, line: str):
    self.tokenizer_obj.read_file = MagicMock(
      return_value=self.expectative_read_file3)
    self.tokenizer_obj.string_separator = MagicMock(
      return_value=self.expectative_string_separator3)

    regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': ID INVALID: You can't start with number\."
    with pytest.raises(LexicalError, match=regex):
      self.tokenizer_obj.analise_line(line)

  @pytest.mark.parametrize("line", ["inputs/literal_not_closed.txt"])
  def test_first_symbol_is_number_error_with_analise_line(self, line: str):
    self.tokenizer_obj.read_file = MagicMock(
      return_value=self.expectative_read_file4)
    self.tokenizer_obj.string_separator = MagicMock(
      return_value=self.expectative_string_separator4)

    regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Text or char not closed\."
    with pytest.raises(LexicalError, match=regex):
      self.tokenizer_obj.analise_line(line)

  @pytest.mark.parametrize("line", ["inputs/opened_delimiter.txt"])
  def test_number_delimiters_error_with_analise_line(self, line: str):
    self.tokenizer_obj.read_file = MagicMock(
        return_value=self.expectative_read_file5)
    self.tokenizer_obj.string_separator = MagicMock(
        return_value=self.expectative_string_separator5)
    regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Delimiter was opened and was not closed\."
    with pytest.raises(LexicalError, match=regex):
      self.tokenizer_obj.analise_line(line)

  @pytest.mark.parametrize("line", ["inputs/closed_delimiter.txt"])
  def test_number_delimiters_error_with_analise_line(self, line: str):
    self.tokenizer_obj.read_file = MagicMock(
        return_value=self.expectative_read_file5)
    self.tokenizer_obj.string_separator = MagicMock(
        return_value=self.expectative_string_separator5)
    regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Delimiter was opened and was not closed\."
    with pytest.raises(LexicalError, match=regex):
      self.tokenizer_obj.analise_line(line)
=======
from src.errors.error import LexicalError
from src.lexical_analyzer.tokenizer import Tokenizer
from src.lexical_analyzer.utils.lexer import Lexer
from src.lexical_analyzer.utils.symbol_table import SymbolTable
from src.lexical_analyzer.utils.token_factory import TokenTypeFactory
from src.lexical_analyzer.utils.token_list import TokenListTable


class TestLexicalTokenizer:
    def setup_method(self, method):
        self.symbol_table = SymbolTable()
        self.token_type_factory = TokenTypeFactory(self.symbol_table)
        self.token_list_table = TokenListTable(self.token_type_factory)
        self.lexer = Lexer()
        self.tokenizer_obj = Tokenizer(
            self.lexer,
            self.token_list_table,
            self.symbol_table,
            self.token_type_factory,
        )
        self.expectative_line_division_operator = [
            ("(", 0, 1),
            ("a", 1, 1),
            ("==", 3, 1),
            ("b", 6, 1),
            ("!=", 8, 1),
            ("c", 11, 1),
            (")", 12, 1),
            ("(", 14, 1),
            ("g", 15, 1),
            ("<=", 17, 1),
            ("d", 20, 1),
            (">=", 22, 1),
            ("e", 25, 1),
            (")", 26, 1),
        ]
        self.expectative_line_division_float = [
            ("angulo", 0, 1),
            ("=", 7, 1),
            ("144.0", 9, 1),
            (";", 14, 1),
        ]
        self.expectative_line_multiple_delimiters = [
            ("var", 0, 1),
            ("inteiro", 4, 1),
            (":", 12, 1),
            ("lado", 14, 1),
            (",", 19, 1),
            ("altura", 21, 1),
            (";", 28, 1),
        ]
        self.expectative_line_comment = []
        self.expectative_line_condition = [
            ("(", 0, 1),
            ("se", 1, 1),
            ("(", 3, 1),
            ("lado", 4, 1),
            ("%", 9, 1),
            ("2", 11, 1),
            (")", 12, 1),
            ("==", 14, 1),
            ("0", 17, 1),
            (")", 18, 1),
        ]
        self.expectative_string_separator1 = [
            ("inicio", 0, 1),
            ("avancar", 2, 3),
            ("150", 10, 3),
            (";", 13, 3),
            ("girar_direita", 2, 4),
            ("90", 16, 4),
            (";", 18, 4),
            ("avancar", 2, 6),
            ("150", 10, 6),
            (";", 13, 6),
            ("girar_direita", 2, 7),
            ("90", 16, 7),
            (";", 18, 7),
            ("avancar", 2, 9),
            ("150", 10, 9),
            (";", 13, 9),
            ("girar_direita", 2, 10),
            ("90", 16, 10),
            (";", 18, 10),
            ("avancar", 2, 12),
            ("150", 10, 12),
            (";", 13, 12),
            ("girar_direita", 2, 13),
            ("90", 16, 13),
            (";", 18, 13),
            ("fim", 0, 14),
        ]
        self.expectative_read_file1 = [
            ("inicio", 1),
            ("  // Desenha as quatro arestas do quadrado", 2),
            ("  avancar 150;", 3),
            ("  girar_direita 90;", 4),
            ("", 5),
            ("  avancar 150;", 6),
            ("  girar_direita 90;", 7),
            ("", 8),
            ("  avancar 150;", 9),
            ("  girar_direita 90;", 10),
            ("", 11),
            ("  avancar 150;", 12),
            ("  girar_direita 90;", 13),
            ("fim", 14),
        ]
        self.expectative_string_separator2 = [('val', 0, 1), ('@', 3, 1), ('doção', 4, 1)]
        self.expectative_read_file2 = [("val@doção", 1)]
        self.expectative_read_file3 = [("1test", 1)]
        self.expectative_string_separator3 = [("1test", 0, 1)]
        self.expectative_string_separator4 = [('"', 0, 1), ("1test", 1, 1)]
        self.expectative_read_file4 = [('"1test', 1)]
        self.expectative_string_separator5 = [("(", 0, 1), ("(", 1, 1), (")", 2, 1)]
        self.expectative_read_file5 = [([("(()", 1)])]
        self.expectative_string_separator6 = [("(", 0, 1), (")", 1, 1), (")", 2, 1)]
        self.expectative_read_file5 = [([("())", 1)])]

    @pytest.mark.parametrize("line", [[("(a == b != c) (g <= d >= e)", 1)]])
    def test_operators_with_string_separator(self, line: list[tuple[str, int]]):
        token_list = self.tokenizer_obj.string_separator(line)

        assert token_list[0] == self.expectative_line_division_operator[0]
        assert token_list[1] == self.expectative_line_division_operator[1]
        assert token_list[2] == self.expectative_line_division_operator[2]
        assert token_list[3] == self.expectative_line_division_operator[3]
        assert token_list[4] == self.expectative_line_division_operator[4]
        assert token_list[5] == self.expectative_line_division_operator[5]
        assert token_list[6] == self.expectative_line_division_operator[6]
        assert token_list[7] == self.expectative_line_division_operator[7]
        assert token_list[8] == self.expectative_line_division_operator[8]
        assert token_list[9] == self.expectative_line_division_operator[9]
        assert token_list[10] == self.expectative_line_division_operator[10]
        assert token_list[11] == self.expectative_line_division_operator[11]

    @pytest.mark.parametrize("line", [[("angulo = 144.0;", 1)]])
    def test_float_with_string_separator(self, line: list[tuple[str, int]]):
        token_list = self.tokenizer_obj.string_separator(line)

        assert token_list[0] == self.expectative_line_division_float[0]
        assert token_list[1] == self.expectative_line_division_float[1]
        assert token_list[2] == self.expectative_line_division_float[2]
        assert token_list[3] == self.expectative_line_division_float[3]

    @pytest.mark.parametrize("line", [[("var inteiro : lado , altura ;", 1)]])
    def test_multiple_delimiter_with_string_separator(
        self, line: list[tuple[str, int]]
    ):
        token_list = self.tokenizer_obj.string_separator(line)

        assert token_list[0] == self.expectative_line_multiple_delimiters[0]
        assert token_list[1] == self.expectative_line_multiple_delimiters[1]
        assert token_list[2] == self.expectative_line_multiple_delimiters[2]
        assert token_list[3] == self.expectative_line_multiple_delimiters[3]
        assert token_list[4] == self.expectative_line_multiple_delimiters[4]
        assert token_list[5] == self.expectative_line_multiple_delimiters[5]
        assert token_list[6] == self.expectative_line_multiple_delimiters[6]

    @pytest.mark.parametrize("line", [[("// simplesmente um comentário", 1)]])
    def test_multiple_delimiter_with_string_separator(
        self, line: list[tuple[str, int]]
    ):
        token_list = self.tokenizer_obj.string_separator(line)

        assert token_list == self.expectative_line_comment

    @pytest.mark.parametrize("line", [[("(se(lado % 2) == 0)", 1)]])
    def test_par_with_string_separator(self, line: list[tuple[str, int]]):
        token_list = self.tokenizer_obj.string_separator(line)

        assert token_list[0] == self.expectative_line_condition[0]
        assert token_list[1] == self.expectative_line_condition[1]
        assert token_list[2] == self.expectative_line_condition[2]
        assert token_list[3] == self.expectative_line_condition[3]
        assert token_list[4] == self.expectative_line_condition[4]
        assert token_list[5] == self.expectative_line_condition[5]
        assert token_list[6] == self.expectative_line_condition[6]
        assert token_list[7] == self.expectative_line_condition[7]
        assert token_list[8] == self.expectative_line_condition[8]
        assert token_list[9] == self.expectative_line_condition[9]

    @pytest.mark.parametrize("line", ["inputs/entrada1.txt"])
    def test_list_token_and_symbols_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file1
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator1
        )

        isNone = self.tokenizer_obj.analise_line(line)

        assert isNone is None

    @pytest.mark.parametrize("line", ["inputs/char_invalido.txt"])
    def test_unknown_symbol_error_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file2
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator2
        )

        regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Symbol not known to the compiler\."
        with pytest.raises(LexicalError, match=regex):
          self.tokenizer_obj.analise_line(line)

    @pytest.mark.parametrize("line", ["inputs/first_char_is_number_on_id.txt"])
    def test_first_symbol_is_number_error_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file3
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator3
        )

        regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': ID INVALID: You can't start with number\."
        with pytest.raises(LexicalError, match=regex):
            self.tokenizer_obj.analise_line(line)

    @pytest.mark.parametrize("line", ["inputs/literal_not_closed.txt"])
    def test_first_symbol_is_number_error_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file4
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator4
        )

        regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Text or char not closed\."
        with pytest.raises(LexicalError, match=regex):
            self.tokenizer_obj.analise_line(line)

    @pytest.mark.parametrize("line", ["inputs/opened_delimiter.txt"])
    def test_number_delimiters_error_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file5
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator5
        )
        regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - ' .*? ': Delimiter was opened and was not closed\."
        with pytest.raises(LexicalError, match=regex):
            self.tokenizer_obj.analise_line(line)

    @pytest.mark.parametrize("line", ["inputs/closed_delimiter.txt"])
    def test_number_delimiters_error_with_analise_line(self, line: str):
        self.tokenizer_obj.read_file = MagicMock(
            return_value=self.expectative_read_file5
        )
        self.tokenizer_obj.string_separator = MagicMock(
            return_value=self.expectative_string_separator5
        )
        regex = r"\[Error ErrorType\.LEXICAL\] \(line \d+, column \d+\) \| symbol - '\s?.+?\s?': Delimiter was opened and was not closed\."
        with pytest.raises(LexicalError, match=regex):
            self.tokenizer_obj.analise_line(line)
>>>>>>> feat-lexical
