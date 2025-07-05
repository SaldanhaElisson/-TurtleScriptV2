
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type_):
        if name in self.symbols:
            raise Exception(f"Erro: Variável '{name}' já declarada.")
        self.symbols[name] = type_

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Erro: Variável '{name}' não declarada.")
        return self.symbols[name]