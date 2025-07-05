# Como tô criando a árvore sintática, vou criar a simulação de classes que representam os nós da árvore.

class Program:
    def __init__(self, declarations, commands):
        self.declarations = declarations
        self.commands = commands

class VariableDeclaration:
    def __init__(self, var_type, names):
        self.var_type = var_type
        self.names = names

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Assignment:
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

class IfStatement:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class RepeatLoop:
    def __init__(self, count, body):
        self.count = count
        self.body = body

class Command:
    def __init__(self, name, args=[]):
        self.name = name
        self.args = args

class Literal:
    def __init__(self, value, type_):
        self.value = value
        self.type_ = type_

class VariableReference:
    def __init__(self, name):
        self.name = name

class Comment:
    def __init__(self, text):
        self.text = text