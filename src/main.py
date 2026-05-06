import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from antlr4 import *
from grammar.NetLangLexer import NetLangLexer
from grammar.NetLangParser import NetLangParser

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/main.py <archivo.txt>")
        sys.exit(1)

    input_stream = FileStream(sys.argv[1])
    lexer = NetLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = NetLangParser(tokens)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() == 0:
        print("✓ Parse exitoso. No se encontraron errores sintácticos.")
        print(tree.toStringTree(recog=parser))
    else:
        print(f"✗ Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) sintáctico(s).")

main()
