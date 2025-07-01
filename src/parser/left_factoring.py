def left_factoring_concise(grammar_rules_dict):
    """
    Applies left factoring to grammar rules to remove common prefixes.
    This version uses more concise Python features like list comprehensions and setdefault.

    Args:
        grammar_rules_dict (dict): A dictionary where keys are non-terminals (LHS)
                                   and values are lists of their productions (RHS).
                                   Example: {'A': [['a', 'D', 'F'], ['a', 'C', 'V'], ['k']]}

    Returns:
        dict: The updated grammar rules dictionary after applying left factoring.
              Example: {'A': [['a', "A'"], ['k']], "A'": [['D', 'F'], ['C', 'V']]}
    """
    factored_grammar = {}
    newly_generated_rules_temp = {}

    for current_non_terminal in list(grammar_rules_dict.keys()):
        all_productions_for_nt = grammar_rules_dict[current_non_terminal]

        productions_by_first_symbol = {}
        for production_sequence in all_productions_for_nt:
            first_symbol = production_sequence[0] if production_sequence else None
            productions_by_first_symbol.setdefault(first_symbol, []).append(production_sequence)

        new_productions_for_current_nt = []

        for common_prefix_symbol, productions_in_group in productions_by_first_symbol.items():
            if common_prefix_symbol is None:
                new_productions_for_current_nt.extend(productions_in_group)
                continue

            if len(productions_in_group) > 1:

                generated_non_terminal_suffix = f"{current_non_terminal}'"
                while (generated_non_terminal_suffix in grammar_rules_dict) or \
                        (generated_non_terminal_suffix in newly_generated_rules_temp):
                    generated_non_terminal_suffix += "'"

                new_productions_for_current_nt.append([common_prefix_symbol, generated_non_terminal_suffix])

                suffixes_for_new_nt = [
                    original_production[1:] for original_production in productions_in_group
                ]
                newly_generated_rules_temp[generated_non_terminal_suffix] = suffixes_for_new_nt
            else:
                new_productions_for_current_nt.extend(productions_in_group)  # Use extend for flat list addition

        factored_grammar[current_non_terminal] = new_productions_for_current_nt

    factored_grammar.update(newly_generated_rules_temp)

    return factored_grammar