
import sys
from pprint import pprint

from src.lexical_analyzer.tokenizer import Tokenizer
from src.lexical_analyzer.utils.lexer import Lexer
from src.lexical_analyzer.utils.symbol_table import SymbolTable
from src.lexical_analyzer.utils.token_factory import TokenTypeFactory
from src.lexical_analyzer.utils.token_list import TokenListTable
from src.code_generator.generator import CodeGenerator
from tests.test_semantic_analyzer import AST_Input_1, AST_Input_2, AST_Input_3, AST_Input_4 


def main(args):
    if not args:
        raise ValueError("no input file")
    path = args[0]
    symbol_table = SymbolTable()
    token_type_factory = TokenTypeFactory(symbol_table)
    token_list_table = TokenListTable(token_type_factory)
    lexer = Lexer()
    tokenizer_obj = Tokenizer(lexer, token_list_table, symbol_table, token_type_factory)
    tokenizer_obj.analise_line(path)


    generator = CodeGenerator()

    print("\nGERAÇÃO DO CÓDIGO 1: \n")
    python_code = generator.generate(AST_Input_1)
    print(python_code)

    print("\nGERAÇÃO DO CÓDIGO 2: \n")
    python_code = generator.generate(AST_Input_2)
    print(python_code)

    print("\nGERAÇÃO DO CÓDIGO 3: \n")
    python_code = generator.generate(AST_Input_3)
    print(python_code)

    print("\n GERAÇÃO DO CÓDIGO 4: \n")
    python_code = generator.generate(AST_Input_4)
    print(python_code)


if __name__ == "__main__":
    main(sys.argv[1:])
