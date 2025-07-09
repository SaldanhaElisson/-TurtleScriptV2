from typing import Dict

from src.parser.calculate_first_set import calculate_first_set_for_sequence


def calculate_follow_sets(grammar_rules: Dict, start_symbol: str, first_sets: Dict) -> Dict:
    follow_sets = {nt: set() for nt in grammar_rules}
    follow_sets[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar_rules.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in grammar_rules:
                        rest = production[i + 1:]
                        if rest:
                            first_rest = calculate_first_set_for_sequence(rest, grammar_rules,
                                                                          set(first_sets.keys()) - set(
                                                                              grammar_rules.keys()),
                                                                          first_sets)
                            old_size = len(follow_sets[symbol])
                            follow_sets[symbol].update(first_rest - {'#'})
                            if '#' in first_rest:
                                follow_sets[symbol].update(follow_sets[lhs])
                            if len(follow_sets[symbol]) > old_size:
                                changed = True
                        else:
                            old_size = len(follow_sets[symbol])
                            follow_sets[symbol].update(follow_sets[lhs])
                            if len(follow_sets[symbol]) > old_size:
                                changed = True

    return follow_sets
