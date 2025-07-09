import unittest
from src.parser.calculate_follow_set import compute_all_follows

class TestFollowSets(unittest.TestCase):

    def test_simple_grammar_no_epsilon(self):
        # Gramática:
        # S -> A B
        # A -> a
        # B -> b
        # Expected: FOLLOW(S) = {$}
        #           FOLLOW(A) = {b}
        #           FOLLOW(B) = {$}
        grammar_rules = {
            'S': [['A', 'B']],
            'A': [['a']],
            'B': [['b']]
        }
        non_terminals = {'S', 'A', 'B'}
        terminal_symbols = {'a', 'b'}
        start_symbol = 'S'

        # FIRST sets pre-calculados (necessários para FOLLOW)
        first_sets = {
            'a': {'a'}, 'b': {'b'}, '#': {'#'},
            'A': {'a'},
            'B': {'b'},
            'S': {'a'}
        }

        expected_follows = {
            'S': {'$'},
            'A': {'b'}, # FOLLOW(A) porque A B, FIRST(B) = {b}
            'B': {'$'}  # FOLLOW(B) porque S -> A B, B é o último, então FOLLOW(B) = FOLLOW(S)
        }

        result = compute_all_follows(start_symbol, grammar_rules, non_terminals, first_sets)
        for nt, expected_set in expected_follows.items():
            self.assertIn(nt, result)
            self.assertEqual(result[nt], expected_set)

    def test_grammar_with_epsilon_in_beta(self):
        # Gramática:
        # S -> A B C
        # A -> a
        # B -> b | #
        # C -> c
        # Expected: FOLLOW(S) = {$}
        #           FOLLOW(A) = {b, c} (b do FIRST(B), c do FIRST(C) se B é epsilon)
        #           FOLLOW(B) = {c} (c do FIRST(C) ou FOLLOW(S) se C é epsilon - mas C não é)
        #           FOLLOW(C) = {$}
        grammar_rules = {
            'S': [['A', 'B', 'C']],
            'A': [['a']],
            'B': [['b'], ['#']],
            'C': [['c']]
        }
        non_terminals = {'S', 'A', 'B', 'C'}
        terminal_symbols = {'a', 'b', 'c'}
        start_symbol = 'S'

        first_sets = {
            'a': {'a'}, 'b': {'b'}, 'c': {'c'}, '#': {'#'},
            'A': {'a'},
            'B': {'b', '#'},
            'C': {'c'},
            'S': {'a'}
        }

        expected_follows = {
            'S': {'$'},
            'A': {'b', 'c'}, # FIRST(B)={b,#}, B pode ser epsilon, então FIRST(C)={c} também entra.
            'B': {'c'},      # FIRST(C)={c}
            'C': {'$'}       # C é o último em S -> ABC, então FOLLOW(C)=FOLLOW(S)
        }

        result = compute_all_follows(start_symbol, grammar_rules, non_terminals, first_sets)
        for nt, expected_set in expected_follows.items():
            self.assertIn(nt, result)
            self.assertEqual(result[nt], expected_set)

    def test_grammar_with_left_recursion_removed_style(self):
        # Gramática (após remoção de recursão à esquerda):
        # E  -> T E'
        # E' -> + T E' | #
        # T  -> F T'
        # T' -> * F T' | #
        # F  -> ( E ) | id
        # Expected:
        # FOLLOW(E)  = {$, ')'}
        # FOLLOW(E') = {$, ')'} (E' é último em E, E' é último em E' -> + T E', então FOLLOW(E') = FOLLOW(E))
        # FOLLOW(T)  = {+, $, ')'} (FOLLOW(T) de E->T E', FIRST(E')={+,#}, se E' é # então FOLLOW(E))
        # FOLLOW(T') = {+, $, ')'} (T' é último em T, T' é último em T' -> * F T', então FOLLOW(T') = FOLLOW(T))
        # FOLLOW(F)  = {*, +, $, ')'} (FOLLOW(F) de T->F T', FIRST(T')={*,#}, se T' é # então FOLLOW(T))

        grammar_rules = {
            'E': [['T', 'E_prime']],
            'E_prime': [['+', 'T', 'E_prime'], ['#']],
            'T': [['F', 'T_prime']],
            'T_prime': [['*', 'F', 'T_prime'], ['#']],
            'F': [['(', 'E', ')'], ['id']]
        }
        non_terminals = {'E', 'E_prime', 'T', 'T_prime', 'F'}
        terminal_symbols = {'+', '*', '(', ')', 'id'}
        start_symbol = 'E'

        # FIRST sets pre-calculados para esta gramática
        first_sets = {
            '+': {'+'}, '*': {'*'}, '(': {'('}, ')': {')'}, 'id': {'id'}, '#': {'#'},
            'F': {'(', 'id'},
            'T_prime': {'*', '#'},
            'T': {'(', 'id'},
            'E_prime': {'+', '#'},
            'E': {'(', 'id'}
        }

        expected_follows = {
            'E': {'$', ')'},
            'E_prime': {'$', ')'},
            'T': {'+', '$', ')'},
            'T_prime': {'+', '$', ')'},
            'F': {'*', '+', '$', ')'}
        }

        result = compute_all_follows(start_symbol, grammar_rules, non_terminals, first_sets)
        for nt, expected_set in expected_follows.items():
            self.assertIn(nt, result)
            self.assertEqual(result[nt], expected_set, f"Falha em FOLLOW({nt}): Esperado {expected_set}, Obtido {result[nt]}")


    def test_grammar_with_mutual_recursion_for_follow(self):
        # Gramática com dependência mútua para FOLLOW
        # S -> A B
        # A -> c
        # B -> d | S
        # Expected:
        # FOLLOW(S) = {$, d} (d de B->S e $ de S ser start_symbol)
        # FOLLOW(A) = {d, $} (de S->AB, FOLLOW(A) = FIRST(B) = {d} se B não tem epsilon. Mas B tem 'S', então FOLLOW(B) = FOLLOW(S))
        # FOLLOW(B) = {$, d} (de S->AB, B é o último, então FOLLOW(B) = FOLLOW(S) = {$, d})

        grammar_rules = {
            'S': [['A', 'B']],
            'A': [['c']],
            'B': [['d'], ['S']]
        }
        non_terminals = {'S', 'A', 'B'}
        terminal_symbols = {'c', 'd'}
        start_symbol = 'S'

        first_sets = {
            'c': {'c'}, 'd': {'d'}, '#': {'#'},
            'A': {'c'},
            'B': {'d', 'c'},
            'S': {'c'}
        }

        expected_follows = {
            'S': {'$'},
            'A': {'d', 'c'},
            'B': {'$'}
        }

        result = compute_all_follows(start_symbol, grammar_rules, non_terminals, first_sets)
        for nt, expected_set in expected_follows.items():
            self.assertIn(nt, result)
            self.assertEqual(result[nt], expected_set, f"Falha em FOLLOW({nt}): Esperado {expected_set}, Obtido {result[nt]}")

