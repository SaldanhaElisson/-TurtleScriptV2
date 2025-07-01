# Conteúdo COMPLETO de src/parser/calculate_first_set.py
# (Remova qualquer outra coisa que possa estar lá, a menos que seja outra função ou import necessário)

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

    # Rule 1: If the current symbol is a terminal
    if current_symbol in terminal_symbols:
        first_result_set.add(current_symbol)
        return first_result_set
    # Rule 3: If the current symbol is epsilon itself
    elif current_symbol == '#':
        first_result_set.add('#')
        return first_result_set

    # Rule 2: If the current symbol is a non-terminal
    if current_symbol in grammar_rules:
        # Get the FIRST set of the non-terminal from the cache if available.
        first_of_current_symbol = first_sets_cache.get(current_symbol, set())

        first_result_set.update(s for s in first_of_current_symbol if s != '#')

        if '#' in first_of_current_symbol and len(symbol_sequence) > 1:
            rest_of_sequence_first = calculate_first_set_for_sequence(
                symbol_sequence[1:], grammar_rules, terminal_symbols, first_sets_cache
            )
            first_result_set.update(rest_of_sequence_first)
        elif '#' in first_of_current_symbol and len(symbol_sequence) == 1:
            first_result_set.add('#')
    else: # Este 'else' é o tratamento para símbolos desconhecidos / literais
        first_result_set.add(current_symbol)

    return first_result_set