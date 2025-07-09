from typing import List, Set, Dict


def calculate_first_set_for_sequence(sequence: List[str], grammar_rules: Dict,
                                     terminal_symbols: Set[str], first_sets: Dict) -> Set[str]:
    if not sequence:
        return {'#'}  # Epsilon

    result = set()

    for symbol in sequence:
        if symbol in terminal_symbols:
            result.add(symbol)
            break
        else:
            symbol_first = first_sets.get(symbol, set())
            result.update(symbol_first - {'#'})
            if '#' not in symbol_first:
                break
    else:
        result.add('#')

    return result

def calculate_first_sets(grammar_rules: Dict, terminal_symbols: Set[str]) -> Dict:
    """Calcula os conjuntos FIRST para todos os símbolos."""
    first_sets = {}

    for terminal in terminal_symbols:
        first_sets[terminal] = {terminal}

    for non_terminal in grammar_rules:
        first_sets[non_terminal] = set()

    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar_rules.items():
            for production in productions:
                if not production or production == ['#']:
                    if '#' not in first_sets[lhs]:
                        first_sets[lhs].add('#')
                        changed = True
                else:
                    old_size = len(first_sets[lhs])
                    prod_first = calculate_first_set_for_sequence(production, grammar_rules, terminal_symbols,
                                                                  first_sets)
                    first_sets[lhs].update(prod_first)
                    if len(first_sets[lhs]) > old_size:
                        changed = True

    return first_sets

