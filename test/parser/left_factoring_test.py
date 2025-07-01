import unittest

from src.parser.left_factoring import left_factoring_concise


class TestLeftFactoringConcise(unittest.TestCase):

    def test_basic_left_factoring(self):
        # Enter A -> aDF | aCV | k
        # Expected: A -> aA' | k,
        # A' -> DF | CV
        input_grammar = {
            'A': [['a', 'D', 'F'], ['a', 'C', 'V'], ['k']]
        }
        expected_output = {
            'A': [['a', "A'"], ['k']],
            "A'": [['D', 'F'], ['C', 'V']]
        }
        self.assertEqual(left_factoring_concise(input_grammar), expected_output)

    def test_no_left_factoring(self):
        # Enter: S -> aA | bB
        # Expected: none
        input_grammar = {
            'S': [['a', 'A'], ['b', 'B']]
        }
        expected_output = {
            'S': [['a', 'A'], ['b', 'B']]
        }
        self.assertEqual(left_factoring_concise(input_grammar), expected_output)

    def test_multiple_common_prefixes(self):
        # Enter: A -> xY | xZ | aB | aC | D
        # Expected: A -> xA' | aA'' | D, A' -> Y | Z, A'' -> B | C
        input_grammar = {
            'A': [['x', 'Y'], ['x', 'Z'], ['a', 'B'], ['a', 'C'], ['D']]
        }

        result = left_factoring_concise(input_grammar)

        self.assertIn(['D'], result['A'])
        self.assertEqual(len([p for p in result['A'] if p[0] == 'x']), 1)
        self.assertEqual(len([p for p in result['A'] if p[0] == 'a']), 1)

        # Encontra os novos não-terminais gerados
        new_nt_x = [p[1] for p in result['A'] if p[0] == 'x'][0]
        new_nt_a = [p[1] for p in result['A'] if p[0] == 'a'][0]

        self.assertIn(['Y'], result[new_nt_x])
        self.assertIn(['Z'], result[new_nt_x])
        self.assertEqual(len(result[new_nt_x]), 2)  # Deve ter 2 produções

        self.assertIn(['B'], result[new_nt_a])
        self.assertIn(['C'], result[new_nt_a])
        self.assertEqual(len(result[new_nt_a]), 2)  # Deve ter 2 produções
        self.assertEqual(len(result.keys()), 3)  # A, A', A''

    def test_empty_grammar(self):
        input_grammar = {}
        expected_output = {}
        self.assertEqual(left_factoring_concise(input_grammar), expected_output)

    def test_production_with_no_suffix(self):

        input_grammar = {
            'A': [['a'], ['a', 'X']]
        }
        result = left_factoring_concise(input_grammar)

        self.assertEqual(len(result['A']), 1)
        self.assertEqual(result['A'][0][0], 'a')

        new_nt = result['A'][0][1]
        self.assertIn(new_nt, result)

        self.assertIn([], result[new_nt])
        self.assertIn(['X'], result[new_nt])
        self.assertEqual(len(result[new_nt]), 2)

    def test_grammar_with_multiple_non_terminals(self):
        input_grammar = {
            'S': [['A', 'B'], ['x']],
            'A': [['a', 'C'], ['a', 'D'], ['b']],
            'B': [['e'], ['f']]
        }
        expected_output = {
            'S': [['A', 'B'], ['x']],
            'A': [['a', "A'"], ['b']],
            "A'": [['C'], ['D']],
            'B': [['e'], ['f']]
        }
        self.assertEqual(left_factoring_concise(input_grammar), expected_output)

    def test_complex_nesting_of_suffixes(self):

        input_grammar = {
            'A': [['a', 'b', 'c'], ['a', 'b', 'd'], ['a', 'x', 'y']]
        }
        result = left_factoring_concise(input_grammar)

        self.assertEqual(len(result['A']), 1)
        self.assertEqual(result['A'][0][0], 'a')

        new_nt = result['A'][0][1]
        self.assertIn(new_nt, result)

        self.assertIn(['b', 'c'], result[new_nt])
        self.assertIn(['b', 'd'], result[new_nt])
        self.assertIn(['x', 'y'], result[new_nt])
        self.assertEqual(len(result[new_nt]), 3)