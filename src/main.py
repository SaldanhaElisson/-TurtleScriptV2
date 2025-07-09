from src.code_generator.generator import CodeGenerator
from src.lexical_analyzer.tokenizer import Tokenizer
from src.lexical_analyzer.utils import TokenTypeFactory, TokenListTable, SymbolTable, Lexer
from src.parser.ast_nodes import ParserLL1, pretty_print_ast_util
from src.semantic_analyzer.analyzer import analyze_program


class TurtleScriptCompiler:
    def __init__(self):
        self.symbol_table_instance = SymbolTable()
        self.lexer_instance = Lexer()
        self.token_factory_instance = TokenTypeFactory(self.symbol_table_instance)
        self.token_list_instance = TokenListTable(self.token_factory_instance)
        self.generator = CodeGenerator()

        self.tokenizer = Tokenizer(
            lexer=self.lexer_instance,
            token_list=self.token_list_instance,
            symbol_table=self.symbol_table_instance,
            token_factory=self.token_factory_instance,
        )

    def compile_script(self, path):
        self.tokenizer.analise_line(path)
        print(self.token_list_instance.get_tokens())
        parser = ParserLL1(self.token_list_instance.get_tokens())
        try:
            ast = parser.parse()
            print("Árvore Sintática Abstrata (AST) gerada com sucesso:")
            print(ast)

            print("\n--- Estrutura da AST (Pretty Print) ---")
            pretty_print_ast_util(ast)

            analyze_program(ast)

            result = self.generator.generate(ast)

            return result
        except SyntaxError as e:
            print(f"✗ Erro de sintaxe: {e}")
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")


def main():
    compiler = TurtleScriptCompiler()

    generated_python_code = compiler.compile_script("../examples/example.txt")

    if generated_python_code:
        print("\n--- CÓDIGO PYTHON GERADO ---\n")
        print(generated_python_code)
    else:
        print("\nNenhum código Python gerado devido a erros.")


if __name__ == "__main__":
    main()