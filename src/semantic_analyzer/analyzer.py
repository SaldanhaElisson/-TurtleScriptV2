from src.semantic_analyzer.syntatic_tree import BinaryExpression, Literal, VariableReference, Assignment, Command, RepeatLoop, Comment, IfStatement, WhileLoop
from src.semantic_analyzer.symbol_table import SymbolTable

def infer_expression_type(expr, symbol_table):
    if isinstance(expr, Literal):
        return expr.type_
    
    elif isinstance(expr, VariableReference):
        return symbol_table.lookup(expr.name)
    
    elif isinstance(expr, BinaryExpression):
        left_type = infer_expression_type(expr.left, symbol_table)
        right_type = infer_expression_type(expr.right, symbol_table)

        if expr.operator in ['+', '-', '*', '/', '%']:
            if expr.operator == '/':
                return 'real'
            
            if expr.operator == '%':
                return 'inteiro'
            
            if left_type == 'inteiro' and right_type == 'inteiro':
                return 'inteiro'
            
            if ('real' in [left_type, right_type]):
                return 'real'
            
            raise Exception(f"Erro: Operador '{expr.operator}' só aceita inteiros ou reais.")

        elif expr.operator in ['>', '<', '==']:
            if left_type == right_type:
                return 'logico'
            
            raise Exception(f"Erro: Comparação inválida entre '{left_type}' e '{right_type}'.")

    else:
        raise Exception(f"Erro: Tipo de expressão não suportada: {type(expr)}")

command_signature = {
    "avancar": ["inteiro"],
    "recuar": ["inteiro"],
    "girar_direita": ["inteiro"],
    "girar_esquerda": ["inteiro"],
    "ir_para": ["inteiro", "inteiro"],
    "levantar_caneta": [],
    "abaixar_caneta": [],
    "definir_cor": ["texto"],
    "definir_espessura": ["inteiro"],
    "limpar_tela": [],
    "cor_de_fundo": ["texto"],
    "escrever": ["texto"],
    "posicao_atual": [],
}

def analyze_assignment(cmd, symbol_table):
    var_type = symbol_table.lookup(cmd.var_name)
    expr_type = infer_expression_type(cmd.expression, symbol_table)

    if var_type != expr_type:
        raise Exception(f"Erro: Atribuição: variável '{cmd.var_name}' é do tipo '{var_type}', mas recebeu '{expr_type}'.")

def analyze_command_call(cmd, symbol_table):
    if cmd.name not in command_signature:
        raise Exception(f"Erro: Comando '{cmd.name}' não existe.")

    expected_args = command_signature[cmd.name]

    args = cmd.args if isinstance(cmd.args, list) else [cmd.args]

    if len(expected_args) != len(args):
        raise Exception(f"Erro: Comando '{cmd.name}' espera {len(expected_args)} argumento(s), mas recebeu {len(args)}.")

    for expected_type, arg in zip(expected_args, args):
        actual_type = infer_expression_type(arg, symbol_table)

        if actual_type != expected_type:
            raise Exception(f"Erro: Comando '{cmd.name}' esperava argumento '{expected_type}' mas recebeu '{actual_type}'.")


def analyze_repeat_loop(cmd, symbol_table):
    print(cmd.count, symbol_table)
    count_type = infer_expression_type(cmd.count, symbol_table)

    if count_type != 'inteiro':
        raise Exception("Erro: O 'repita' deve receber uma expressão do tipo inteiro.")
    
    for inner_cmd in cmd.body:
        analyze_command(inner_cmd, symbol_table)

def analyze_command(cmd, symbol_table):
    if isinstance(cmd, Assignment):
        analyze_assignment(cmd, symbol_table)

    elif isinstance(cmd, Command):
        analyze_command_call(cmd, symbol_table)

    elif isinstance(cmd, RepeatLoop):
        analyze_repeat_loop(cmd, symbol_table)

    elif isinstance(cmd, IfStatement):
        analyze_if_statement(cmd, symbol_table)

    elif isinstance(cmd, WhileLoop):
        analyze_while_loop(cmd, symbol_table)

    elif isinstance(cmd, Comment):
        pass
        
    else:
        raise Exception(f"Erro: Tipo de comando não reconhecido: {type(cmd)}")
    
def analyze_if_statement(cmd, symbol_table):
    cond_type = infer_expression_type(cmd.condition, symbol_table)
    if cond_type != 'logico':
        raise Exception("Erro: A condição do 'se' deve ser do tipo lógico.")
    
    for inner_cmd in cmd.true_branch:
        analyze_command(inner_cmd, symbol_table)

    if cmd.false_branch:
        for inner_cmd in cmd.false_branch:
            analyze_command(inner_cmd, symbol_table)

def analyze_while_loop(cmd, symbol_table):
    cond_type = infer_expression_type(cmd.condition, symbol_table)
    if cond_type != 'logico':
        raise Exception("Erro: A condição do 'enquanto' deve ser do tipo lógico.")
    
    for inner_cmd in cmd.body:
        analyze_command(inner_cmd, symbol_table)

def analyze_program(program):
    symbol_table = SymbolTable()

    for decl in program.declarations:
        for name in decl.names:
            symbol_table.declare(name, decl.var_type)

    for cmd in program.commands:
        analyze_command(cmd, symbol_table)
