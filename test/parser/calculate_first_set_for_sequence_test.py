import unittest
from src.parser.calculate_first_set import calculate_first_set_for_sequence
from src.parser.calculate_first_set import compute_all_first_sets_for_grammar

class TestFirstSets(unittest.TestCase):

    def test_calculate_first_set_for_sequence_terminals(self):
        grammar = {}
        terminals = {'a', 'b', 'c'}
        cache = {}
        self.assertEqual(calculate_first_set_for_sequence(['a', 'B'], grammar, terminals, cache), {'a'})
        self.assertEqual(calculate_first_set_for_sequence(['b'], grammar, terminals, cache), {'b'})

    def test_calculate_first_set_for_sequence_epsilon(self):
        grammar = {}
        terminals = set()
        cache = {}
        self.assertEqual(calculate_first_set_for_sequence([], grammar, terminals, cache), {'#'})
        self.assertEqual(calculate_first_set_for_sequence(['#'], grammar, terminals, cache), {'#'})

    def test_calculate_first_set_for_sequence_non_terminals(self):

        grammar = {
            'S': [['A', 'B']],
            'A': [['a'], ['#']],
            'B': [['b']]
        }
        terminals = {'a', 'b', 'c'}
        # Cache simulado com FIRST de A e B já calculados
        cache = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'A': {'a', '#'},
            'B': {'b'}
        }
        # FIRST(A B) = (FIRST(A) - {#}) U FIRST(B) se # in FIRST(A)
        # FIRST(A B) = ({'a'} - {#}) U {'b'} = {'a', 'b'}
        self.assertEqual(calculate_first_set_for_sequence(['A', 'B'], grammar, terminals, cache), {'a', 'b'})


        grammar2 = {
            'S': [['X', 'Y']],
            'X': [['x']],
            'Y': [['y']]
        }
        terminals2 = {'x', 'y'}
        cache2 = {
            'x': {'x'}, 'y': {'y'}, '#': {'#'},
            'X': {'x'},
            'Y': {'y'}
        }
        self.assertEqual(calculate_first_set_for_sequence(['X', 'Y'], grammar2, terminals2, cache2), {'x'})


        grammar3 = {
            'S': [['A', 'B']],
            'A': [['#']],
            'B': [['#']]
        }
        terminals3 = set()
        cache3 = {
            '#': {'#'},
            'A': {'#'},
            'B': {'#'}
        }
        # FIRST(A B) = {#}
        self.assertEqual(calculate_first_set_for_sequence(['A', 'B'], grammar3, terminals3, cache3), {'#'})


    def test_compute_all_first_sets_grammar_simple(self):

        grammar = {
            'S': [['A', 'B']],
            'A': [['a']],
            'B': [['b']]
        }
        non_terminals = {'S', 'A', 'B'}
        terminal_symbols = {'a', 'b'}
        expected_firsts = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'A': {'a'},
            'B': {'b'},
            'S': {'a'}
        }
        result = compute_all_first_sets_for_grammar(grammar, non_terminals, terminal_symbols)
        # Usamos assertDictEqual para comparar dicionários
        # Para conjuntos, a ordem não importa
        for key in expected_firsts:
            self.assertIn(key, result) # Garante que a chave existe no resultado
            self.assertEqual(result[key], expected_firsts[key])

    def test_compute_all_first_sets_grammar_with_epsilon(self):
        # Gramática com epsilon e dependências
        # S -> A B
        # A -> a | #
        # B -> b | #
        grammar = {
            'S': [['A', 'B']],
            'A': [['a'], ['#']],
            'B': [['b'], ['#']]
        }
        non_terminals = {'S', 'A', 'B'}
        terminal_symbols = {'a', 'b'}
        expected_firsts = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'A': {'a', '#'},
            'B': {'b', '#'},
            'S': {'a', 'b', '#'} # FIRST(A B) = (FIRST(A)-{#}) U FIRST(B) se # in FIRST(A) = ({'a'}) U {'b', '#'} = {'a', 'b', '#'}
        }
        result = compute_all_first_sets_for_grammar(grammar, non_terminals, terminal_symbols)
        for key in expected_firsts:
            self.assertIn(key, result)
            self.assertEqual(result[key], expected_firsts[key])

    def test_compute_all_first_sets_grammar_indirect_epsilon(self):
        # Teste com epsilon indireto
        # X -> Y Z
        # Y -> y | #
        # Z -> z | #
        grammar = {
            'X': [['Y', 'Z']],
            'Y': [['y'], ['#']],
            'Z': [['z'], ['#']]
        }
        non_terminals = {'X', 'Y', 'Z'}
        terminal_symbols = {'y', 'z'}
        expected_firsts = {
            'y': {'y'}, 'z': {'z'}, '#': {'#'},
            'Y': {'y', '#'},
            'Z': {'z', '#'},
            'X': {'y', 'z', '#'} # FIRST(Y Z) = (FIRST(Y)-{#}) U FIRST(Z) se # in FIRST(Y) = ({'y'}) U {'z', '#'} = {'y', 'z', '#'}
        }
        result = compute_all_first_sets_for_grammar(grammar, non_terminals, terminal_symbols)
        for key in expected_firsts:
            self.assertIn(key, result)
            self.assertEqual(result[key], expected_firsts[key])

    def test_compute_all_first_sets_grammar_with_cycles(self):
        # Teste com ciclo simples (requer a iteração de ponto fixo)
        # A -> B c
        # B -> A d | e
        # A gramática precisa ser pré-processada para remover recursão à esquerda
        # Assumimos que o input já está limpo para LL(1), então este teste simula um caso onde
        # a dependência é resolvida por múltiplas iterações.
        # Ex: E -> T E'
        # E' -> + T E' | #
        # T -> F T'
        # T' -> * F T' | #
        # F -> ( E ) | id

        grammar = {
            'E': [['T', 'E_prime']],
            'E_prime': [['+', 'T', 'E_prime'], ['#']],
            'T': [['F', 'T_prime']],
            'T_prime': [['*', 'F', 'T_prime'], ['#']],
            'F': [['(', 'E', ')'], ['id']]
        }
        non_terminals = {'E', 'E_prime', 'T', 'T_prime', 'F'}
        terminal_symbols = {'+', '*', '(', ')', 'id'}

        expected_firsts = {
            '+': {'+'}, '*': {'*'}, '(': {'('}, ')': {')'}, 'id': {'id'}, '#': {'#'},
            'F': {'(', 'id'},
            'T_prime': {'*', '#'},
            'T': {'(', 'id'}, # FIRST(F T_prime) = FIRST(F) = {'(', 'id'}
            'E_prime': {'+', '#'},
            'E': {'(', 'id'} # FIRST(T E_prime) = FIRST(T) = {'(', 'id'}
        }
        result = compute_all_first_sets_for_grammar(grammar, non_terminals, terminal_symbols)
        for key in expected_firsts:
            self.assertIn(key, result)
            self.assertEqual(result[key], expected_firsts[key])

    def test_compute_all_first_sets_empty_grammar(self):
        # Teste com gramática vazia
        grammar = {}
        non_terminals = set()
        terminal_symbols = set()
        expected_firsts = {'#': {'#'}} # Epsilon deve estar lá por padrão
        result = compute_all_first_sets_for_grammar(grammar, non_terminals, terminal_symbols)
        self.assertEqual(result, expected_firsts)

