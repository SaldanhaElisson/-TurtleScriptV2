import unittest
from src.parser.calculate_follow_set import calculate_follow_set

class TestCalculateFollowSet(unittest.TestCase):

    def setUp(self):
        self.grammar1 = {
            'S': [['A', 'B']],
            'A': [['a']],
            'B': [['c']]
        }
        self.start_symbol1 = 'S'
        self.first_sets1 = {
            'a': {'a'},
            'b': {'b'},
            'c': {'c'},
            '#': {'#'},
            'S': {'a'},
            'A': {'a'},
            'B': {'c'}
        }


        self.grammar2 = {
            'S': [['A', 'B']],
            'A': [['a'], ['#']],
            'B': [['b']]
        }
        self.start_symbol2 = 'S'
        self.first_sets2 = {
            'a': {'a'},
            'b': {'b'},
            '#': {'#'},
            'S': {'a', 'b'},
            'A': {'a', '#'},
            'B': {'b'}
        }


        self.grammar3 = {
            'S': [['A', 'B']],
            'A': [['a']],
            'B': [['C']],
            'C': [['c'], ['#']]
        }
        self.start_symbol3 = 'S'
        self.first_sets3 = {
            'a': {'a'},
            'c': {'c'},
            '#': {'#'},
            'S': {'a'},
            'A': {'a'},
            'B': {'c', '#'},
            'C': {'c', '#'}
        }

        self.grammar4 = {
            'E': [['T', 'E\'']],
            'E\'': [['+', 'T', 'E\''], ['#']],
            'T': [['F', 'T\'']],
            'T\'': [['*', 'F', 'T\''], ['#']],
            'F': [['(', 'E', ')'], ['id']]
        }
        self.start_symbol4 = 'E'
        self.first_sets4 = {
            'E': {'(', 'id'},
            'E\'': {'+', '#'},
            'T': {'(', 'id'},
            'T\'': {'*', '#'},
            'F': {'(', 'id'},
            '+': {'+'},
            '*': {'*'},
            '(': {'('},
            ')': {')'},
            'id': {'id'},
            '#': {'#'}
        }

    def test_follow_start_symbol(self):
        self.assertEqual(calculate_follow_set('S', self.start_symbol1, self.grammar1, self.first_sets1), {'$'})

    def test_follow_rule2_terminal(self):
        self.assertEqual(calculate_follow_set('A', self.start_symbol1, self.grammar1, self.first_sets1), {'c'})

    def test_follow_rule3_epsilon_and_follow_lhs(self):

        self.assertEqual(calculate_follow_set('A', self.start_symbol2, self.grammar2, self.first_sets2), {'b', '$'})

    def test_follow_rule3_epsilon_and_follow_lhs_chained(self):

        self.assertEqual(calculate_follow_set('A', self.start_symbol3, self.grammar3, self.first_sets3), {'c'})
        self.assertEqual(calculate_follow_set('B', self.start_symbol3, self.grammar3, self.first_sets3), {'$'})
        self.assertEqual(calculate_follow_set('C', self.start_symbol3, self.grammar3, self.first_sets3), {'$'})

    def test_follow_for_intermediate_non_terminal(self):
        self.assertEqual(calculate_follow_set('B', self.start_symbol1, self.grammar1, self.first_sets1), {'$'})

    def test_follow_complex_grammar_E_prime(self):


        self.assertEqual(calculate_follow_set('E', self.start_symbol4, self.grammar4, self.first_sets4), {')', '$'})
        self.assertEqual(calculate_follow_set('E\'', self.start_symbol4, self.grammar4, self.first_sets4), {')', '$'})

    def test_follow_complex_grammar_T_prime(self):

        self.assertEqual(calculate_follow_set('T', self.start_symbol4, self.grammar4, self.first_sets4),
                         {'+', ')', '$'})
        self.assertEqual(calculate_follow_set('T\'', self.start_symbol4, self.grammar4, self.first_sets4),
                         {'+', ')', '$'})

    def test_follow_complex_grammar_F(self):

        self.assertEqual(calculate_follow_set('F', self.start_symbol4, self.grammar4, self.first_sets4),
                         {'*', '+', ')', '$'})

    def test_non_terminal_not_in_rhs(self):

        grammar_isolated = {'A': [['a']], 'B': [['b']]}
        start_isolated = 'A'
        first_isolated = {'a': {'a'}, 'b': {'b'}, 'A': {'a'}, 'B': {'b'}}


        self.assertEqual(calculate_follow_set('B', start_isolated, grammar_isolated, first_isolated), set())

    def test_recursion_avoidance(self):

        grammar_recursive_A = {
            'S': [['A']],
            'A': [['B', 'A'], ['c']],
            'B': [['b']]
        }
        start_recursive_A = 'S'
        first_recursive_A = {
            'S': {'b', 'c'},
            'A': {'b', 'c'},
            'B': {'b'},
            'b': {'b'},
            'c': {'c'}
        }
        self.assertEqual(calculate_follow_set('A', start_recursive_A, grammar_recursive_A, first_recursive_A), {'$'})
        self.assertEqual(calculate_follow_set('B', start_recursive_A, grammar_recursive_A, first_recursive_A),
                         {'b', 'c'})