def compute_all_follows(start_symbol, grammar_rules, non_terminals, first_sets):
    """
    Calculates the FOLLOW set for all non-terminals in the grammar.

    Args:
        start_symbol (str): The starting non-terminal of the grammar.
        grammar_rules (dict): A dictionary representing the grammar rules
                              (NonTerminal: [list of productions, where each production is a list of symbols]).
        non_terminals (set): A set of all non-terminal symbols in the grammar.
        first_sets (dict): A dictionary containing pre-calculated FIRST sets
                           for all grammar symbols (terminals, non-terminals, and '#').

    Returns:
        dict: A dictionary where keys are non-terminals and values are their calculated FOLLOW sets.
    """

    follows = {nt: set() for nt in non_terminals}
    follows[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for non_terminal_to_compute_follow in non_terminals:
            current_follow_set = follows[non_terminal_to_compute_follow].copy()

            # Itera sobre todas as regras da gramática para encontrar ocorrências do non_terminal_to_compute_follow
            for current_lhs_non_terminal, productions_rhs in grammar_rules.items():
                for production_sequence in productions_rhs:
                    indices_of_target = [i for i, symbol in enumerate(production_sequence)
                                         if symbol == non_terminal_to_compute_follow]

                    for index in indices_of_target:
                        # Pega a sequência de símbolos que vêm DEPOIS do não-terminal alvo
                        beta_sequence = production_sequence[index + 1:]

                        if beta_sequence:
                            first_of_beta = calculate_first_of_sequence(beta_sequence, first_sets)
                            follows[non_terminal_to_compute_follow].update(term for term in first_of_beta if term != '#')

                            # Regra 2: Se '#' está em FIRST(Beta), então FOLLOW(A) = FOLLOW(A) U FOLLOW(LHS)
                            if '#' in first_of_beta:

                                if non_terminal_to_compute_follow != current_lhs_non_terminal:
                                    follows[non_terminal_to_compute_follow].update(
                                        follows.get(current_lhs_non_terminal, set())
                                    )
                        else:

                            if non_terminal_to_compute_follow != current_lhs_non_terminal:
                                follows[non_terminal_to_compute_follow].update(
                                    follows.get(current_lhs_non_terminal, set())
                                )

            if current_follow_set != follows[non_terminal_to_compute_follow]:
                changed = True
    return follows

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
        else:
            result_first.add(symbol)
            all_can_be_epsilon = False
            break

    if all_can_be_epsilon:
        result_first.add('#')

    return result_first