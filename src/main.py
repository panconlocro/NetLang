import sys
from antlr4 import *
from NetLangLexer import NetLangLexer
from NetLangParser import NetLangParser

def main():
    input_stream = FileStream(sys.argv[1])
    lexer = NetLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = NetLangParser(tokens)
    tree = parser.program()
    
    if parser.getNumberOfSyntaxErrors() == 0:
        print("✓ Parse exitoso")
    else:
        print("✗ Errores encontrados")

main()
