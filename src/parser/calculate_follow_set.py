def calculate_follow_set(target_non_terminal, start_symbol, grammar_rules, first_sets):
    """
    Calculates the FOLLOW set for a given non-terminal.

    Args:
        target_non_terminal (str): The non-terminal for which to calculate the FOLLOW set.
        start_symbol (str): The starting non-terminal of the grammar.
        grammar_rules (dict): A dictionary representing the grammar rules
                              (NonTerminal: [list of productions]).
        first_sets (dict): A dictionary containing pre-calculated FIRST sets
                           for all grammar symbols (e.g., {'A': {'a', 'b'}}).

    Returns:
        set: A set of terminals in the FOLLOW set for the target_non_terminal.
             Returns an empty set if no FOLLOW symbols are found.
    """
    follow_set_result = set()

    if target_non_terminal == start_symbol:
        follow_set_result.add('$')

    for current_lhs_non_terminal, productions_rhs in grammar_rules.items():
        for production_sequence in productions_rhs:
            indices_of_target = [i for i, symbol in enumerate(production_sequence) if symbol == target_non_terminal]

            for index in indices_of_target:
                beta_sequence = production_sequence[index + 1:]

                if beta_sequence:

                    first_of_beta = calculate_first_of_sequence(beta_sequence,
                                                                first_sets)

                    follow_set_result.update(term for term in first_of_beta if term != '#')

                    if '#' in first_of_beta:

                        if target_non_terminal != current_lhs_non_terminal:
                            follow_set_result.update(
                                calculate_follow_set(current_lhs_non_terminal, start_symbol, grammar_rules, first_sets)
                            )
                else:
                    if target_non_terminal != current_lhs_non_terminal:
                        # Recursive call, passing all necessary parameters
                        follow_set_result.update(
                            calculate_follow_set(current_lhs_non_terminal, start_symbol, grammar_rules, first_sets)
                        )

    return follow_set_result


def calculate_first_of_sequence(symbols_sequence, first_sets):
    """Calculates the FIRST set for a sequence of symbols."""
    result_first = set()
    all_can_be_epsilon = True

    for symbol in symbols_sequence:
        if symbol in first_sets:
            result_first.update(s for s in first_sets[symbol] if s != '#')
            if '#' not in first_sets[symbol]:
                all_can_be_epsilon = False
                break
        else:  # It's a terminal or unknown symbol
            result_first.add(symbol)
            all_can_be_epsilon = False
            break

    if all_can_be_epsilon:
        result_first.add('#')  

    return result_first

