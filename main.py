import sys
from pprint import pprint

from scripts.tokenizer import Tokenizer
from structs.lexer import Lexer
from structs.symbol_table import SymbolTable
from structs.token_factory import TokenTypeFactory
from structs.token_list import TokenListTable


def main(args):
    if not args:
        raise ValueError("no input file")
    path = args[0]
    symbol_table = SymbolTable()
    token_type_factory = TokenTypeFactory(symbol_table)
    token_list_table = TokenListTable(token_type_factory)
    lexer = Lexer()
    tokenizer_obj = Tokenizer(lexer, token_list_table, symbol_table,
                              token_type_factory)
    tokenizer_obj.analise_line(path)

    print("List<TokenList>: \n")
    pprint(token_list_table.get_tokens())
    print("\n")
    print("List<SymbolsTable>: \n")
    pprint(symbol_table.get_symbols())
    print("\n")

if __name__ == '__main__':
    main(sys.argv[1:])