import unittest
from unittest.mock import patch, MagicMock
from src.parser.parser import create_ll1_parse_table
from src.parser.parser import parse_ll1_string


class TestLL1ParseTable(unittest.TestCase):

    @patch('src.parser.calculate_first_set.calculate_first_set_for_sequence')
    def test_simple_ll1_grammar(self, mock_calculate_first_set_for_sequence):
        # S -> a B
        # B -> b | #
        grammar_rules = {
            'S': [['a', 'B']],
            'B': [['b'], ['#']]
        }
        non_terminals = {'S', 'B'}
        terminal_symbols = {'a', 'b'}


        mock_calculate_first_set_for_sequence.side_effect = [
            {'a'},  # FIRST(['a', 'B'])
            {'b'},  # FIRST(['b'])
            {'#'}  # FIRST(['#'])
        ]

        first_sets = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'S': {'a'},
            'B': {'b', '#'}
        }

        follow_sets = {
            'S': {'$'},
            'B': {'$'}
        }

        # Tabela de Parsing Esperada
        expected_parse_table = {
            'B': {'$': 'B->#', 'a': '', 'b': 'B->b'},
            'S': {'$': '', 'a': 'S->a B', 'b': ''}
        }

        sorted_non_terminals = sorted(list(non_terminals))
        sorted_terminals_cols = sorted(list(terminal_symbols) + ['$'])
        final_expected_table = {
            nt: {t: expected_parse_table.get(nt, {}).get(t, '') for t in sorted_terminals_cols}
            for nt in sorted_non_terminals
        }

        parse_table, is_ll1 = create_ll1_parse_table(
            grammar_rules, first_sets, follow_sets, terminal_symbols, non_terminals
        )

        self.assertTrue(is_ll1)  # A gramática deve ser LL(1)
        self.assertEqual(parse_table, final_expected_table)

    @patch('src.parser.calculate_first_set.calculate_first_set_for_sequence')
    def test_grammar_with_epsilon_production(self, mock_calculate_first_set_for_sequence):
        # S -> A B
        # A -> a | #
        # B -> b
        grammar_rules = {
            'S': [['A', 'B']],
            'A': [['a'], ['#']],
            'B': [['b']]
        }
        non_terminals = {'S', 'A', 'B'}
        terminal_symbols = {'a', 'b'}

        mock_calculate_first_set_for_sequence.side_effect = [
            {'a', 'b'},  # FIRST(['A', 'B'])
            {'a'},  # FIRST(['a'])
            {'#'},  # FIRST(['#'])
            {'b'}  # FIRST(['b'])
        ]

        first_sets = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'S': {'a', 'b'},
            'A': {'a', '#'},
            'B': {'b'}
        }

        # FOLLOW(S) = {$}
        # FOLLOW(A) = {b} (pois A B, FIRST(B) = {b})
        # FOLLOW(B) = {$} (pois S -> A B, B é o último, então FOLLOW(B) = FOLLOW(S))
        follow_sets = {
            'S': {'$'},
            'A': {'b'},
            'B': {'$'}
        }

        expected_parse_table = {
            'A': {'a': 'A->a', 'b': 'A->#', '$': ''},  # A-># entra em 'b' porque 'b' está em FOLLOW(A)
            'B': {'a': '', 'b': 'B->b', '$': ''},
            'S': {'a': 'S->A B', 'b': 'S->A B', '$': ''}  # S->AB, FIRST(AB)={a,b}
        }

        sorted_non_terminals = sorted(list(non_terminals))
        sorted_terminals_cols = sorted(list(terminal_symbols) + ['$'])
        final_expected_table = {
            nt: {t: expected_parse_table.get(nt, {}).get(t, '') for t in sorted_terminals_cols}
            for nt in sorted_non_terminals
        }

        parse_table, is_ll1 = create_ll1_parse_table(
            grammar_rules, first_sets, follow_sets, terminal_symbols, non_terminals
        )

        self.assertTrue(is_ll1)  # Deve ser LL(1)
        self.assertEqual(parse_table, final_expected_table)

    @patch('src.parser.calculate_first_set.calculate_first_set_for_sequence')
    def test_grammar_with_ll1_conflict(self, mock_calculate_first_set_for_sequence):
        # Gramática com conflito LL(1) (NÃO é LL(1))
        # Ex: S -> a B | a C
        # FIRST(a B) = {a}
        # FIRST(a C) = {a}
        # Isso causa um conflito na célula (S, a) da tabela.
        grammar_rules = {
            'S': [['a', 'B'], ['a', 'C']],
            'B': [['b']],
            'C': [['c']]
        }
        non_terminals = {'S', 'B', 'C'}
        terminal_symbols = {'a', 'b', 'c'}

        # Mock dos retornos
        mock_calculate_first_set_for_sequence.side_effect = [
            {'a'},  # FIRST(['a', 'B'])
            {'a'},  # FIRST(['a', 'C'])
            {'b'},  # FIRST(['b'])
            {'c'}  # FIRST(['c'])
        ]

        first_sets = {
            'a': {'a'}, 'b': {'b'}, 'c': {'c'}, '#': {'#'},
            'S': {'a'},
            'B': {'b'},
            'C': {'c'}
        }

        follow_sets = {
            'S': {'$'},
            'B': {'$'},
            'C': {'$'}
        }

        expected_parse_table_partial = {
            'S': {'a': 'S->a B | S->a C', 'b': '', 'c': '', '$': ''},  # Conflito esperado
            'B': {'a': '', 'b': 'B->b', 'c': '', '$': ''},
            'C': {'a': '', 'b': '', 'c': 'C->c', '$': ''}
        }

        sorted_non_terminals = sorted(list(non_terminals))
        sorted_terminals_cols = sorted(list(terminal_symbols) + ['$'])
        final_expected_table = {
            nt: {t: expected_parse_table_partial.get(nt, {}).get(t, '') for t in sorted_terminals_cols}
            for nt in sorted_non_terminals
        }

        parse_table, is_ll1 = create_ll1_parse_table(
            grammar_rules, first_sets, follow_sets, terminal_symbols, non_terminals
        )

        self.assertFalse(is_ll1)  # A gramática NÃO deve ser LL(1)
        self.assertEqual(parse_table, final_expected_table)

    @patch('src.parser.calculate_first_set.calculate_first_set_for_sequence')
    def test_empty_grammar(self, mock_calculate_first_set_for_sequence):
        grammar_rules = {}
        non_terminals = set()
        terminal_symbols = set()

        mock_calculate_first_set_for_sequence.side_effect = []

        first_sets = {'#': {'#'}}
        follow_sets = {}

        expected_parse_table = {}  # A tabela deve ser vazia

        parse_table, is_ll1 = create_ll1_parse_table(
            grammar_rules, first_sets, follow_sets, terminal_symbols, non_terminals
        )

        self.assertTrue(is_ll1)
        self.assertEqual(parse_table, expected_parse_table)


class TestLL1Parser(unittest.TestCase):

    # Exemplo de gramática de expressões aritméticas (já processada)
    # E  -> T E'
    # E' -> + T E' | #
    # T  -> F T'
    # T' -> * F T' | #
    # F  -> ( E ) | id
    def setUp(self):
        # Configurações comuns para os testes
        self.grammar_rules = {
            'E': [['T', 'E_prime']],
            'E_prime': [['+', 'T', 'E_prime'], ['#']],
            'T': [['F', 'T_prime']],
            'T_prime': [['*', 'F', 'T_prime'], ['#']],
            'F': [['(', 'E', ')'], ['id']]
        }
        self.non_terminals = {'E', 'E_prime', 'T', 'T_prime', 'F'}
        self.terminal_symbols = {'+', '*', '(', ')', 'id'}
        self.start_symbol = 'E'


        self.parsing_table = {
            'E': {
                '(': 'E->T E_prime',
                'id': 'E->T E_prime',
                '+': '', '*': '', ')': '', '$': ''
            },
            'E_prime': {
                '+': 'E_prime->+ T E_prime',
                ')': 'E_prime->#',
                '$': 'E_prime->#'
            },
            'T': {
                '(': 'T->F T_prime',
                'id': 'T->F T_prime',
                '+': '', '*': '', ')': '', '$': ''
            },
            'T_prime': {
                '*': 'T_prime->* F T_prime',
                '+': 'T_prime->#',
                ')': 'T_prime->#',
                '$': 'T_prime->#'
            },
            'F': {
                '(': 'F->( E )',
                'id': 'F->id',
                '+': '', '*': '', ')': '', '$': ''
            }
        }
        self.is_ll1_grammar = True  # Para a maioria dos testes, assumimos que é LL(1)

    def test_valid_simple_expression(self):
        input_tokens = ['id', '+', 'id']
        expected_result = "\nCadeia Válida!"
        result = parse_ll1_string(
            self.parsing_table, self.is_ll1_grammar, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )
        self.assertEqual(result, expected_result)

    def test_valid_complex_expression(self):
        input_tokens = ['(', 'id', '*', 'id', ')']
        expected_result = "\nCadeia Válida!"
        result = parse_ll1_string(
            self.parsing_table, self.is_ll1_grammar, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )
        self.assertEqual(result, expected_result)

    def test_invalid_missing_terminal(self):
        input_tokens = ['id', '+']
        expected_result_prefix = "\nCadeia Inválida! Nenhuma regra encontrada na tabela de parsing para (T, $)."  # Ou outro erro dependendo da ordem
        result = parse_ll1_string(
            self.parsing_table, self.is_ll1_grammar, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )
        self.assertTrue(result.startswith("\nCadeia Inválida!"))

    def test_invalid_unmatched_terminal(self):
        # Teste uma cadeia inválida: "id * + id"
        input_tokens = ['id', '*', '+', 'id']
        # A expectativa foi ajustada para refletir o comportamento real da função
        expected_result_prefix = "\nCadeia Inválida! Nenhuma regra encontrada na tabela de parsing para (F, +)."

        result = parse_ll1_string(
            self.parsing_table, self.is_ll1_grammar, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )
        self.assertEqual(result, expected_result_prefix)  # Usar assertEqual para correspondência exata, ou startswith se o prefixo for suficiente

    def test_invalid_non_ll1_grammar(self):

        input_tokens = ['a', 'b']
        invalid_ll1_grammar_flag = False

        result = parse_ll1_string(
            self.parsing_table, invalid_ll1_grammar_flag, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )
        self.assertEqual(result, "\nErro: A gramática não é LL(1). Não é possível realizar o parsing.")

    def test_invalid_empty_input(self):
        input_tokens = []
        result = parse_ll1_string(
            self.parsing_table, self.is_ll1_grammar, self.terminal_symbols,
            self.non_terminals, self.start_symbol, input_tokens
        )

        self.assertTrue(result.startswith("\nCadeia Inválida!"))

    def test_invalid_unexpected_symbol_on_stack(self):

        malformed_parsing_table = {
            'E': {'id': 'E->X', '+': ''},

        }

        input_tokens = ['id']
        result = parse_ll1_string(
            malformed_parsing_table, True, self.terminal_symbols,
            {'E'}, 'E', input_tokens  # Non_terminals não inclui 'X'
        )
        self.assertTrue(result.startswith("\nCadeia Inválida! Símbolo desconhecido na pilha: 'X'."))
