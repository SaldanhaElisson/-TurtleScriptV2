from enum import Enum

from src.lexical_analyzer.utils import KeyWords, Delimiters, Operators
from src.lexical_analyzer.utils.token import Token
from src.semantic_analyzer.syntatic_tree import VariableDeclaration, Assignment, Command, RepeatLoop, WhileLoop, \
    IfStatement, VariableReference, Literal, BinaryExpression, CommentNode, Program



class ParserLL1:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token | None:
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def advance(self) -> Token | None:
        if self.current < len(self.tokens):
            token = self.tokens[self.current]
            self.current += 1
            return token
        return None

    def expect(self, *expected_types: str) -> Token:

        token = self.peek()
        if not token:
            raise SyntaxError(f"Expected one of {expected_types}, but reached end of file.")
        if token.token_type in expected_types:
            return self.advance()
        else:
            raise SyntaxError(
                f"Expected one of {expected_types}, got {token.token_type} ('{token.lexeme}') at line {token.line}, column {token.column}")

    def parse(self) -> Program:

        self.expect(Delimiters.START.name)

        declarations = []
        while self.peek() and self.peek().token_type == KeyWords.VAR.name:
            declarations.append(self.parse_variable_declaration())

        commands = []
        while self.peek() and self.peek().token_type != Delimiters.END.name:
            if self.peek() is None:
                raise SyntaxError("Expected 'fim' but reached end of file.")
            commands.append(self.parse_command())

        self.expect(Delimiters.END.name)

        return Program(declarations, commands)

    def parse_variable_declaration(self) -> VariableDeclaration:
        """
        Regra: VariableDeclaration -> 'var' TYPE ':' IDENTIFIER (',' IDENTIFIER)* ';'
        """
        self.expect(KeyWords.VAR.name)

        type_token = self.expect(KeyWords.INTEGER.name, KeyWords.FLOAT.name, KeyWords.TEXT.name, KeyWords.BOOLEAN.name)
        var_type = type_token.lexeme

        self.expect(Delimiters.COLON.name)

        names = []
        names.append(self.expect('IDENTIFIER').lexeme)

        while self.peek() and self.peek().token_type == Delimiters.COMMA.name:
            self.advance()
            names.append(self.expect('IDENTIFIER').lexeme)

        self.expect(Delimiters.SEMICOLON.name)
        return VariableDeclaration(var_type, names)

    def parse_command(self):
        """
        Regra: Command -> Assignment | IfStatement | WhileLoop | RepeatLoop | FunctionCall
        """
        current_token = self.peek()
        if not current_token:
            raise SyntaxError("Unexpected end of tokens while parsing command.")

        if current_token.token_type == 'IDENTIFIER':
            next_token = self.tokens[self.current + 1] if self.current + 1 < len(self.tokens) else None

            if next_token and next_token.token_type == Operators.ASSIGN.name:
                return self.parse_assignment()
            else:
                return self.parse_function_call()
        elif current_token.token_type == KeyWords.IF.name:
            return self.parse_if_statement()
        elif current_token.token_type == KeyWords.WHILE.name:
            return self.parse_while_loop()
        elif current_token.token_type == KeyWords.REPEAT.name:
            return self.parse_repeat_loop()
        else:
            raise SyntaxError(
                f"Unexpected token in command: {current_token.token_type} ('{current_token.lexeme}') at line {current_token.line}, column {current_token.column}")

    def parse_assignment(self) -> Assignment:

        var_name = self.expect('IDENTIFIER').lexeme
        self.expect(Operators.ASSIGN.name)
        expression = self.parse_expression()
        self.expect(Delimiters.SEMICOLON.name)
        return Assignment(var_name, expression)

    def parse_function_call(self) -> Command:

        function_name = self.expect('IDENTIFIER').lexeme
        args = []

        if self.peek() and self.peek().token_type == Delimiters.LEFT_PAR.name:
            self.advance()
            if self.peek().token_type != Delimiters.RIGHT_PAR.name:
                args.append(self.parse_expression())
                while self.peek() and self.peek().token_type == Delimiters.COMMA.name:
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(Delimiters.RIGHT_PAR.name)
        elif self.peek() and self.peek().token_type != Delimiters.SEMICOLON.name:
            args.append(self.parse_expression())

        self.expect(Delimiters.SEMICOLON.name)
        return Command(function_name, args)

    def parse_if_statement(self) -> IfStatement:

        self.expect(KeyWords.IF.name)
        condition = self.parse_expression()
        self.expect(KeyWords.THEN.name)

        true_branch = self.parse_command_block([KeyWords.ELSE.name, KeyWords.END_IF.name])

        false_branch = None
        if self.peek() and self.peek().token_type == KeyWords.ELSE.name:
            self.advance()
            false_branch = self.parse_command_block([KeyWords.END_IF.name])

        self.expect(KeyWords.END_IF.name)
        return IfStatement(condition, true_branch, false_branch)

    def parse_while_loop(self) -> WhileLoop:

        self.expect(KeyWords.WHILE.name)
        condition = self.parse_expression()
        self.expect(KeyWords.DO.name)

        body = self.parse_command_block([KeyWords.END_WHILE.name])

        self.expect(KeyWords.END_WHILE.name)
        return WhileLoop(condition, body)

    def parse_repeat_loop(self) -> RepeatLoop:

        self.expect(KeyWords.REPEAT.name)
        count = self.parse_expression()
        self.expect(KeyWords.DO.name)

        body = self.parse_command_block([KeyWords.END_REPEAT.name])

        self.expect(KeyWords.END_REPEAT.name)
        return RepeatLoop(count, body)

    def parse_command_block(self, stop_tokens: list[str]) -> list:

        commands = []
        while self.peek() and self.peek().token_type not in stop_tokens:
            if self.peek() is None:
                raise SyntaxError(f"Unexpected end of file inside a block. Expected one of {stop_tokens}")
            commands.append(self.parse_command())
        return commands

    def parse_expression(self):

        return self.parse_comparison()

    def parse_comparison(self):

        left = self.parse_addition()

        while self.peek() and self.peek().token_type in [
            Operators.EQUAL.name, Operators.NOT_EQUAL.name, Operators.LESS_THAN.name,
            Operators.LESS_EQUAL.name, Operators.GREATER_THAN.name, Operators.GREATER_EQUAL.name
        ]:
            operator_token = self.advance()
            right = self.parse_addition()
            left = BinaryExpression(left, operator_token.lexeme, right)
        return left

    def parse_addition(self):

        left = self.parse_multiplication()

        while self.peek() and self.peek().token_type in [Operators.PLUS.name, Operators.MINUS.name]:
            operator_token = self.advance()
            right = self.parse_multiplication()
            left = BinaryExpression(left, operator_token.lexeme, right)
        return left

    def parse_multiplication(self):

        left = self.parse_primary()

        while self.peek() and self.peek().token_type in [Operators.MULTIPLICATION.name, Operators.DIVISIVE.name]:
            operator_token = self.advance()
            right = self.parse_primary()
            left = BinaryExpression(left, operator_token.lexeme, right)
        return left

    def parse_primary(self):

        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of tokens while parsing primary expression.")

        if token.token_type == 'IDENTIFIER':
            return VariableReference(self.advance().lexeme)
        elif token.token_type == 'INTEGER':
            value = int(self.advance().lexeme)
            return Literal(value, KeyWords.INTEGER.lexeme)
        elif token.token_type == 'FLOAT':
            value = float(self.advance().lexeme)
            return Literal(value, KeyWords.FLOAT.lexeme)
        elif token.token_type == 'STRING' or token.token_type == KeyWords.TEXT.name:
            value = token.lexeme.strip('"')
            self.advance()
            return Literal(value, KeyWords.TEXT.lexeme)
        elif token.token_type == 'BOOLEAN':
            value = (token.lexeme == 'verdadeiro')
            self.advance()
            return Literal(value, KeyWords.BOOLEAN.lexeme)
        elif token.token_type == Delimiters.LEFT_PAR.name:
            self.advance()
            expr = self.parse_expression()
            self.expect(Delimiters.RIGHT_PAR.name)
            return expr
        else:
            raise SyntaxError(
                f"Unexpected token in primary expression: {token.token_type} ('{token.lexeme}') at line {token.line}, column {token.column}")

def pretty_print_ast_util(node, indent=0):
    spaces = "  " * indent

    if isinstance(node, Program):
        print(f"{spaces}Program:")
        print(f"{spaces}  Declarations:")
        for decl in node.declarations:
            pretty_print_ast_util(decl, indent + 2)
        print(f"{spaces}  Commands:")
        for cmd in node.commands:
            pretty_print_ast_util(cmd, indent + 2)

    elif isinstance(node, VariableDeclaration):
        print(f"{spaces}VariableDeclaration(type='{node.var_type}', names={node.names})")

    elif isinstance(node, Assignment):
        print(f"{spaces}Assignment(var='{node.var_name}'):")
        pretty_print_ast_util(node.expression, indent + 1)

    elif isinstance(node, BinaryExpression):
        print(f"{spaces}BinaryExpression(op='{node.operator}'):")
        print(f"{spaces}  Left:")
        pretty_print_ast_util(node.left, indent + 2)
        print(f"{spaces}  Right:")
        pretty_print_ast_util(node.right, indent + 2)

    elif isinstance(node, IfStatement):
        print(f"{spaces}IfStatement:")
        print(f"{spaces}  Condition:")
        pretty_print_ast_util(node.condition, indent + 2)
        print(f"{spaces}  TrueBranch:")
        for stmt in node.true_branch:
            pretty_print_ast_util(stmt, indent + 3)
        if node.false_branch:
            print(f"{spaces}  FalseBranch:")
            for stmt in node.false_branch:
                pretty_print_ast_util(stmt, indent + 3)

    elif isinstance(node, WhileLoop):
        print(f"{spaces}WhileLoop:")
        print(f"{spaces}  Condition:")
        pretty_print_ast_util(node.condition, indent + 2)
        print(f"{spaces}  Body:")
        for stmt in node.body:
            pretty_print_ast_util(stmt, indent + 3)

    elif isinstance(node, RepeatLoop):
        print(f"{spaces}RepeatLoop:")
        print(f"{spaces}  Count:")
        pretty_print_ast_util(node.count, indent + 2)
        print(f"{spaces}  Body:")
        for stmt in node.body:
            pretty_print_ast_util(stmt, indent + 3)

    elif isinstance(node, Command):
        print(f"{spaces}Command(name='{node.name}', args={len(node.args)}):")
        for arg in node.args:
            pretty_print_ast_util(arg, indent + 1)

    elif isinstance(node, Literal):
        print(f"{spaces}Literal(value='{node.value}', type_='{node.type_}')")

    elif isinstance(node, VariableReference):
        print(f"{spaces}VariableReference(name='{node.name}')")

    elif isinstance(node, CommentNode):
        print(f"{spaces}CommentNode(text='{node.text}')")

    else:
        print(f"{spaces}UNKNOWN_NODE: {type(node).__name__} = {node}")


def main():

    tokens_input = [
        Token(token_type='START', lexeme='inicio', line=1, column=0),
        Token(token_type='IDENTIFIER', lexeme='avancar', line=3, column=2),
        Token(token_type='INTEGER', lexeme='150', line=3, column=10),
        Token(token_type='SEMICOLON', lexeme=';', line=3, column=13),
        Token(token_type='IDENTIFIER', lexeme='girar_direita', line=4, column=2),
        Token(token_type='INTEGER', lexeme='90', line=4, column=16),
        Token(token_type='SEMICOLON', lexeme=';', line=4, column=18),
        Token(token_type='IDENTIFIER', lexeme='avancar', line=6, column=2),
        Token(token_type='INTEGER', lexeme='150', line=6, column=10),
        Token(token_type='SEMICOLON', lexeme=';', line=6, column=13),
        Token(token_type='IDENTIFIER', lexeme='girar_direita', line=7, column=2),
        Token(token_type='INTEGER', lexeme='90', line=7, column=16),
        Token(token_type='SEMICOLON', lexeme=';', line=7, column=18),
        Token(token_type='IDENTIFIER', lexeme='avancar', line=9, column=2),
        Token(token_type='INTEGER', lexeme='150', line=9, column=10),
        Token(token_type='SEMICOLON', lexeme=';', line=9, column=13),
        Token(token_type='IDENTIFIER', lexeme='girar_direita', line=10, column=2),
        Token(token_type='INTEGER', lexeme='90', line=10, column=16),
        Token(token_type='SEMICOLON', lexeme=';', line=10, column=18),
        Token(token_type='IDENTIFIER', lexeme='avancar', line=12, column=2),
        Token(token_type='INTEGER', lexeme='150', line=12, column=10),
        Token(token_type='SEMICOLON', lexeme=';', line=12, column=13),
        Token(token_type='IDENTIFIER', lexeme='girar_direita', line=13, column=2),
        Token(token_type='INTEGER', lexeme='90', line=13, column=16),
        Token(token_type='SEMICOLON', lexeme=';', line=13, column=18),
        Token(token_type='END', lexeme='fim', line=14, column=0),
    ]

    parser = ParserLL1(tokens_input)
    try:
        ast = parser.parse()
        print("Árvore Sintática Abstrata (AST) gerada com sucesso:")
        print(ast)

        print("\n--- Estrutura da AST (Pretty Print) ---")
        pretty_print_ast_util(ast)

    except SyntaxError as e:
        print(f"✗ Erro de sintaxe: {e}")
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")




if __name__ == "__main__":
    main()