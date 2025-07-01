def remove_left_recursion(grammar_rules):
    """
    Eliminates immediate left recursion from grammar rules.
    Args:
        grammar_rules (dict): A dictionary where keys are non-terminals (LHS)
        and values are lists of their productions (RHS).
    Example: {'A': [['A', 'a'], ['b']]}

    Returns:
        dict: The updated grammar rules dictionary without immediate left recursion.
    Example: {'A': [['b', 'A_prime']], 'A_prime': [['a', 'A_prime'], ['#']]}

    """
    newly_generated_rules = {}

    for non_terminal in list(grammar_rules.keys()):
        left_recursive_productions = [
            prod[1:] for prod in grammar_rules[non_terminal] if prod and prod[0] == non_terminal
        ]
        non_left_recursive_productions = [
            prod for prod in grammar_rules[non_terminal] if not prod or prod[0] != non_terminal
        ]

        if left_recursive_productions:
            new_non_terminal = f"{non_terminal}'"
            while new_non_terminal in grammar_rules or new_non_terminal in newly_generated_rules:
                new_non_terminal += "'"

            grammar_rules[non_terminal] = [
                prod + [new_non_terminal] for prod in non_left_recursive_productions
            ]

            newly_generated_rules[new_non_terminal] = [
                prod + [new_non_terminal] for prod in left_recursive_productions
            ]
            newly_generated_rules[new_non_terminal].append(['#'])

    grammar_rules.update(newly_generated_rules)
    return grammar_rules
