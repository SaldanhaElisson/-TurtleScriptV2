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

    for non_terminal in grammar_rules:
        left_recursive_productions = []
        non_left_recursive_productions = []


        for production_rhs in grammar_rules[non_terminal]:
            if production_rhs and production_rhs[0] == non_terminal:
                left_recursive_productions.append(production_rhs[1:])
            else:
                non_left_recursive_productions.append(production_rhs)

        if left_recursive_productions:
            new_non_terminal = non_terminal + "'"
            while new_non_terminal in grammar_rules or new_non_terminal in newly_generated_rules:
                new_non_terminal += "'"


            for i in range(len(non_left_recursive_productions)):
                non_left_recursive_productions[i].append(new_non_terminal)
            grammar_rules[non_terminal] = non_left_recursive_productions


            for i in range(len(left_recursive_productions)):
                left_recursive_productions[i].append(new_non_terminal)
            left_recursive_productions.append(['#'])

            newly_generated_rules[new_non_terminal] = left_recursive_productions

    grammar_rules.update(newly_generated_rules) 

    return grammar_rules