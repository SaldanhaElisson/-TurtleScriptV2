from src.semantic_analyzer.syntatic_tree import RepeatLoop, Command, Comment, VariableDeclaration, Assignment, BinaryExpression, IfStatement, WhileLoop, Literal, VariableReference

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code = []
        self.imports = set()
        
    def add_import(self, module):
        self.imports.add(module)
        
    def add_line(self, line):
        self.code.append("    " * self.indent_level + line)
        
    def increase_indent(self):
        self.indent_level += 1
        
    def decrease_indent(self):
        self.indent_level -= 1

    def generate_output_file(self, code):
        pass
        
    def generate(self, program):
        self.add_import("import turtle")
        
        for decl in program.declarations:
            self.generate_declaration(decl)
            
        for cmd in program.commands:
            self.generate_command(cmd)
            
        imports_code = "\n".join(sorted(self.imports)) + "\n\n"
        main_code = "\n".join(self.code)

        code = imports_code + main_code + "\n\nturtle.done()"

        self.generate_output_file(code)
        
        return code
        
    def generate_declaration(self, decl):
        default_values = {
            "inteiro": "0",
            "real": "0.0",
            "texto": '""',
            "logico": "False"
        }
        
        for name in decl.names:
            self.add_line(f"{name} = {default_values[decl.var_type]}")
            
    def generate_expression(self, expr):
        if isinstance(expr, Literal):
            if expr.type_ == "texto":
                return f'"{expr.value}"'
            return str(expr.value)
            
        elif isinstance(expr, VariableReference):
            return expr.name
            
        elif isinstance(expr, BinaryExpression):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            op = expr.operator
            
            if op == "%":
                return f"math.fmod({left}, {right})"
            return f"({left} {op} {right})"
            
        elif isinstance(expr, Comment):
            self.generate_comment(expr.text)
            
        else:
            raise Exception(f"Tipo de expressão não suportado: {type(expr)}")
            
    def generate_assignment(self, cmd):
        expr_code = self.generate_expression(cmd.expression)
        self.add_line(f"{cmd.var_name} = {expr_code}")
        
    def generate_command_call(self, cmd):
        args = cmd.args if isinstance(cmd.args, list) else [cmd.args]

        args_code = ", ".join(self.generate_expression(arg) for arg in args)
        
        command_mapping = {
            "avancar": "turtle.forward",
            "recuar": "turtle.backward",
            "girar_direita": "turtle.right",
            "girar_esquerda": "turtle.left",
            "ir_para": "turtle.goto",
            "levantar_caneta": "turtle.penup",
            "abaixar_caneta": "turtle.pendown",
            "definir_cor": "turtle.pencolor",
            "definir_espessura": "turtle.pensize",
            "limpar_tela": "turtle.clear",
            "cor_de_fundo": "turtle.bgcolor",
        }
        
        if cmd.name in command_mapping:
            func_name = command_mapping[cmd.name]
            if cmd.args:
                self.add_line(f"{func_name}({args_code})")
            else:
                self.add_line(f"{func_name}()")
        else:
            raise Exception(f"Comando não reconhecido: {cmd.name}")
            
    def generate_repeat_loop(self, cmd):
        count_code = cmd.count
        self.add_line(f"for _ in range(int({count_code})):")
        self.increase_indent()
        
        for inner_cmd in cmd.body:
            print(inner_cmd)
            self.generate_command(inner_cmd)
            
        self.decrease_indent()
        
    def generate_if_statement(self, cmd):
        cond_code = self.generate_expression(cmd.condition)
        self.add_line(f"if {cond_code}:")
        self.increase_indent()
        
        for inner_cmd in cmd.true_branch:
            self.generate_command(inner_cmd)
            
        self.decrease_indent()
        
        if cmd.false_branch:
            self.add_line("else:")
            self.increase_indent()
            
            for inner_cmd in cmd.false_branch:
                self.generate_command(inner_cmd)
                
            self.decrease_indent()
            
    def generate_while_loop(self, cmd):
        cond_code = self.generate_expression(cmd.condition)
        self.add_line(f"while {cond_code}:")
        self.increase_indent()
        
        for inner_cmd in cmd.body:
            self.generate_command(inner_cmd)
            
        self.decrease_indent()
        
    def generate_command(self, cmd):
        if isinstance(cmd, Assignment):
            self.generate_assignment(cmd)
            
        elif isinstance(cmd, Command):
            self.generate_command_call(cmd)
            
        elif isinstance(cmd, RepeatLoop):
            self.generate_repeat_loop(cmd)
            
        elif isinstance(cmd, IfStatement):
            self.generate_if_statement(cmd)
            
        elif isinstance(cmd, WhileLoop):
            self.generate_while_loop(cmd)

        elif isinstance(cmd, Comment):
            self.generate_comment(cmd.text)
            
        else:
            raise Exception(f"Tipo de comando não reconhecido: {type(cmd)}")
        
    def generate_comment(self, comment):
        self.add_line(f"# {comment}")
