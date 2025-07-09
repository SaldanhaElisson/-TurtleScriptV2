
import sys
from pprint import pprint

from src.lexical_analyzer.tokenizer import Tokenizer
from src.lexical_analyzer.utils.lexer import Lexer
from src.lexical_analyzer.utils.symbol_table import SymbolTable
from src.lexical_analyzer.utils.token_factory import TokenTypeFactory
from src.lexical_analyzer.utils.token_list import TokenListTable
from src.code_generator.generator import CodeGenerator
from src.semantic_analyzer.analyzer import analyze_program
from tests.test_semantic_analyzer import AST_Input_1, AST_Input_2, AST_Input_3, AST_Input_4, Error_input


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

    inputs = [
        AST_Input_1, AST_Input_2, AST_Input_3, AST_Input_4, Error_input
    ]

    try:
        for input_ast in inputs:
            print(f"\nANALISANDO O PROGRAMA: output_{inputs.index(input_ast) + 1}")
            analyze_program(input_ast)

            print("ANÁLISE SEMÂNTICA CONCLUÍDA COM SUCESSO!")
            
            print(f"\n GERAÇÃO DO CÓDIGO output_{inputs.index(input_ast) + 1}: \n")
            result = generator.generate(input_ast)

            print(result)
            print("\nGERAÇÃO DE CÓDIGO CONCLUÍDA COM SUCESSO!")
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main(sys.argv[1:])
    
