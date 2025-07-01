import unittest
from src.parser.remove_left_recursion import remove_left_recursion


class TestRemoveLeftRecursion(unittest.TestCase):

    def test_basic_left_recursion(self):
        # Enter A -> Aa | b
        # Expected: A -> bA', A' -> aA' | #
        input_grammar = {
            'A': [['A', 'a'], ['b']]
        }
        expected_output = {
            'A': [['b', 'A\'']],
            'A\'': [['a', 'A\''], ['#']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_no_left_recursion(self):
        # Enter S -> aA | b
        # Expected: S -> aA | b (sem alterações)
        input_grammar = {
            'S': [['a', 'A'], ['b']]
        }
        expected_output = {
            'S': [['a', 'A'], ['b']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_multiple_left_recursive_productions(self):
        # Enter E -> E+T | E-T | T
        # Expected: E -> TA', A' -> +TA' | -TA' | #
        input_grammar = {
            'E': [['E', '+', 'T'], ['E', '-', 'T'], ['T']]
        }
        expected_output = {
            'E': [['T', 'E\'']],
            'E\'': [['+', 'T', 'E\''], ['-', 'T', 'E\''], ['#']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_multiple_non_left_recursive_productions(self):
        # Enter A -> Ax | Ay | B | C
        # Expected: A -> BA' | CA', A' -> xA' | yA' | #
        input_grammar = {
            'A': [['A', 'x'], ['A', 'y'], ['B'], ['C']]
        }
        expected_output = {
            'A': [['B', 'A\''], ['C', 'A\'']],
            'A\'': [['x', 'A\''], ['y', 'A\''], ['#']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_empty_grammar(self):
        input_grammar = {}
        expected_output = {}
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_non_terminal_with_only_left_recursion(self):
        input_grammar = {
            'A': [['A', 'a'], ['A', 'b']]
        }
        expected_output = {
            'A': [],
            'A\'': [['a', 'A\''], ['b', 'A\''], ['#']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)

    def test_complex_grammar(self):
        input_grammar = {
            'S': [['A', 'B'], ['c']],
            'A': [['A', 'x'], ['y']],
            'B': [['z']]
        }
        expected_output = {
            'S': [['A', 'B'], ['c']],
            'A': [['y', 'A\'']],
            'A\'': [['x', 'A\''], ['#']],
            'B': [['z']]
        }
        self.assertEqual(remove_left_recursion(input_grammar), expected_output)