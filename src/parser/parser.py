from src.parser.calculate_first_set import calculate_first_set_for_sequence
def create_ll1_parse_table(grammar_rules, first_sets, follow_sets, terminal_symbols, non_terminals):
    """
    Cria a tabela de parsing LL(1) para uma dada gramática.

    Args:
        grammar_rules (dict): Dicionário das regras da gramática
                              (NãoTerminal: [lista de produções, onde cada produção é uma lista de símbolos]).
                              Deve estar sem recursão à esquerda e fatorada.
        first_sets (dict): Dicionário com os conjuntos FIRST para todos os símbolos (terminais e não-terminais).
        follow_sets (dict): Dicionário com os conjuntos FOLLOW para todos os não-terminais.
        terminal_symbols (set): Conjunto de todos os símbolos terminais na gramática.
        non_terminals (set): Conjunto de todos os símbolos não-terminais na gramática.

    Returns:
        tuple: Uma tupla contendo:
            - dict: A tabela de parsing (ex: {'E': {'id': 'E->TE\'', '+': ''}}).
            - bool: True se a gramática é LL(1), False caso contrário.
    """
    all_terminals_cols = sorted(list(terminal_symbols) + ['$'])
    all_non_terminals_rows = sorted(list(non_terminals))

    parse_table = {nt: {t: '' for t in all_terminals_cols} for nt in all_non_terminals_rows}

    grammar_is_ll1 = True

    for lhs_nt, productions in grammar_rules.items():
        for production_body in productions:
            # Aqui está a chamada para a função FIRST da sequência que será mockada
            production_first_set = calculate_first_set_for_sequence(
                production_body, grammar_rules, terminal_symbols, first_sets
            )

            for terminal in production_first_set:
                if terminal != '#': # Ignora epsilon para esta parte
                    if parse_table[lhs_nt][terminal] == '':
                        parse_table[lhs_nt][terminal] = f"{lhs_nt}->{' '.join(production_body)}"
                    else:
                        grammar_is_ll1 = False
                        parse_table[lhs_nt][terminal] += f" | {lhs_nt}->{' '.join(production_body)}"

            if '#' in production_first_set:
                for terminal in follow_sets.get(lhs_nt, set()):
                    if parse_table[lhs_nt][terminal] == '':
                        parse_table[lhs_nt][terminal] = f"{lhs_nt}->{' '.join(production_body)}"
                    else:
                        grammar_is_ll1 = False
                        parse_table[lhs_nt][terminal] += f" | {lhs_nt}->{' '.join(production_body)}"

    return parse_table, grammar_is_ll1

# --- FIM DA FUNÇÃO create_ll1_parse_table ---
def parse_ll1_string(parsing_table, is_ll1_grammar, terminal_symbols, non_terminals, start_symbol, input_tokens):
    """
    Valida uma sequência de tokens de entrada usando uma tabela de parsing LL(1).

    Args:
        parsing_table (dict): A tabela de parsing LL(1) gerada,
                              no formato {NãoTerminal: {Terminal: "LHS->RHS"}}.
        is_ll1_grammar (bool): True se a gramática é LL(1), False caso contrário.
        terminal_symbols (set): Conjunto de todos os símbolos terminais da gramática.
        non_terminals (set): Conjunto de todos os símbolos não-terminais da gramática.
        start_symbol (str): O símbolo inicial da gramática.
        input_tokens (list): Uma lista de tokens da string de entrada (já tokenizada).

    Returns:
        str: "Valid String!" se a string for aceita, ou uma mensagem de erro detalhada.
    """
    print(f"\n--- Iniciando Análise Sintática para: {' '.join(input_tokens)} ---")

    if not is_ll1_grammar:
        return f"\nErro: A gramática não é LL(1). Não é possível realizar o parsing."

    # Inicializa a pilha: Símbolo inicial no topo, '$' no fundo
    stack = [start_symbol, '$']
    # Inicializa o buffer de entrada: Tokens da entrada + '$' no final
    buffer = input_tokens + ['$']

    print(f"{'Buffer':<20} {'Pilha':<20} {'Ação':<30}")
    print("-" * 70)

    while True:
        current_stack_top = stack[0]
        current_input_token = buffer[0]

        print(f"{' '.join(buffer):<20} {' '.join(stack):<20}", end=" ")

        # 1. Sucesso: Pilha e Buffer vazios (apenas '$')
        if current_stack_top == '$' and current_input_token == '$':
            print(f"{'CADEIA VÁLIDA':<30}")
            print("-" * 70)
            return "\nCadeia Válida!"

        # 2. Topo da Pilha é um Terminal
        elif current_stack_top in terminal_symbols:
            if current_stack_top == current_input_token:
                print(f"Match: {current_stack_top:<20}")
                stack.pop(0)  # Remove do topo da pilha
                buffer.pop(0) # Remove do início do buffer
            else:
                print(f"{'ERRO: Terminal Inesperado':<30}")
                print("-" * 70)
                return (f"\nCadeia Inválida! Símbolo terminal não esperado: "
                        f"Esperado '{current_stack_top}', Recebido '{current_input_token}'.")

        # 3. Topo da Pilha é um Não-Terminal
        elif current_stack_top in non_terminals:
            # Consulta a tabela de parsing
            rule_entry = parsing_table.get(current_stack_top, {}).get(current_input_token, '')

            if rule_entry:
                # Se há uma regra, aplica-a
                print(f"Aplicar Regra: {rule_entry:<20}")
                stack.pop(0) # Remove o Não-Terminal da pilha

                # A regra é no formato "LHS->RHS"
                # Acha o RHS e o divide em símbolos. Trata epsilon.
                lhs, rhs_str = rule_entry.split("->")
                # Se rhs_str é '#', então a produção é epsilon, e nenhum símbolo é empurrado.
                rhs_symbols = rhs_str.strip().split() if rhs_str.strip() != '#' else []

                # Empurra os símbolos do RHS para a pilha, em ordem inversa
                # para que o primeiro símbolo da regra esteja no topo da pilha.
                for symbol in reversed(rhs_symbols):
                    stack.insert(0, symbol)
            else:
                # Nenhuma regra encontrada na tabela para (Não-Terminal, Lookahead)
                print(f"{'ERRO: Sem Regra na Tabela':<30}")
                print("-" * 70)
                return (f"\nCadeia Inválida! Nenhuma regra encontrada na tabela de parsing para "
                        f"({current_stack_top}, {current_input_token}).")
        else:
            # Isso não deveria acontecer com uma gramática bem definida,
            # mas é um fallback para símbolos desconhecidos na pilha.
            print(f"{'ERRO: Símbolo Desconhecido na Pilha':<30}")
            print("-" * 70)
            return f"\nCadeia Inválida! Símbolo desconhecido na pilha: '{current_stack_top}'."