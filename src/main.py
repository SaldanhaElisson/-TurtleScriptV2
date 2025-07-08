import sys
from pprint import pprint

<<<<<<< HEAD
from lexical_analyzer.tokenizer import Tokenizer
from lexical_analyzer.utils.lexer import Lexer
from lexical_analyzer.utils.symbol_table import SymbolTable
from lexical_analyzer.utils.token_factory import TokenTypeFactory
from lexical_analyzer.utils.token_list import TokenListTable
=======
from src.lexical_analyzer.tokenizer import Tokenizer
from src.lexical_analyzer.utils.lexer import Lexer
from src.lexical_analyzer.utils.symbol_table import SymbolTable
from src.lexical_analyzer.utils.token_factory import TokenTypeFactory
from src.lexical_analyzer.utils.token_list import TokenListTable
>>>>>>> feat-lexical


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

<<<<<<< HEAD
    print("List<TokenList>: \n")
    pprint(token_list_table.get_tokens())
    print("\n")
    print("List<SymbolsTable>: \n")
    pprint(symbol_table.get_symbols())
    print("\n")

=======
>>>>>>> feat-lexical

if __name__ == "__main__":
    main(sys.argv[1:])
