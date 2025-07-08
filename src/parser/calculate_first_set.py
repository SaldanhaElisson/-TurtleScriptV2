def calculate_first_set_for_sequence(symbol_sequence, grammar_rules, terminal_symbols, first_sets_cache):
    """
    Recursively calculates the FIRST set for a given sequence of symbols.

    Args:
        symbol_sequence (list): A list of symbols (terminals and/or non-terminals).
        grammar_rules (dict): The grammar rules dictionary mapping non-terminals to productions.
        terminal_symbols (set): A set of all terminal symbols in the grammar.
        first_sets_cache (dict): A dictionary that stores pre-calculated FIRST sets for individual
                                 non-terminals and terminals. This is crucial for recursion
                                 and efficiency.

    Returns:
        set: The calculated FIRST set for the symbol_sequence.
    """
    first_result_set = set()

    if not symbol_sequence:
        first_result_set.add('#')
        return first_result_set

    current_symbol = symbol_sequence[0]

    if current_symbol in terminal_symbols:
        first_result_set.add(current_symbol)
        return first_result_set
    elif current_symbol == '#':
        first_result_set.add('#')
        return first_result_set

    if current_symbol in grammar_rules:

        first_of_current_symbol = first_sets_cache.get(current_symbol, set())

        first_result_set.update(s for s in first_of_current_symbol if s != '#')

        if '#' in first_of_current_symbol and len(symbol_sequence) > 1:
            rest_of_sequence_first = calculate_first_set_for_sequence(
                symbol_sequence[1:], grammar_rules, terminal_symbols, first_sets_cache
            )
            first_result_set.update(rest_of_sequence_first)

        elif '#' in first_of_current_symbol and len(symbol_sequence) == 1:
            first_result_set.add('#')
    else:
        first_result_set.add(current_symbol)

    return first_result_set

def compute_all_first_sets_for_grammar(grammar_rules, non_terminals, terminal_symbols):
    """
    Calculates the FIRST set for all non-terminals in the grammar.

    Args:
        grammar_rules (dict): A dictionary representing the grammar rules
                              (NonTerminal: [list of productions, where each production is a list of symbols]).
                              Example: {'E': [['T', '+', 'E'], ['T']], 'T': [['F', '*', 'T'], ['F']]}
        non_terminals (set): A set of all non-terminal symbols in the grammar.
        terminal_symbols (set): A set of all terminal symbols in the grammar.

    Returns:
        dict: A dictionary where keys are non-terminals and values are their calculated FIRST sets.
    """

    first_sets_cache = {}
    for terminal in terminal_symbols:
        first_sets_cache[terminal] = {terminal}

    first_sets_cache['#'] = {'#'}

    for non_terminal in non_terminals:
        first_sets_cache[non_terminal] = set()


    changed = True
    while changed:
        changed = False
        for non_terminal in non_terminals:
            current_first_set = first_sets_cache[non_terminal].copy()

            for production in grammar_rules.get(non_terminal, []):
                first_of_production = calculate_first_set_for_sequence(
                    production, grammar_rules, terminal_symbols, first_sets_cache
                )
                first_sets_cache[non_terminal].update(first_of_production)

            if current_first_set != first_sets_cache[non_terminal]:
                changed = True

    return first_sets_cache
