import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from antlr4 import *
from grammar.NetLangLexer import NetLangLexer
from grammar.NetLangParser import NetLangParser
from SemanticAnalyzer import SemanticAnalyzer

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/main.py <archivo.txt>")
        sys.exit(1)

    input_stream = FileStream(sys.argv[1], encoding='utf-8')
    lexer = NetLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = NetLangParser(tokens)
    tree = parser.program()

    # Analisis sintactico
    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"✗ Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) sintactico(s). Abortando.")
        sys.exit(1)

    print("✓ Analisis sintactico exitoso")

    # Analisis semantico
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)

    if analyzer.errors:
        print(f"✗ Se encontraron {len(analyzer.errors)} error(es) semantico(s):")
        for error in analyzer.errors:
            print(f"  - {error}")
    else:
        print("✓ Analisis semantico exitoso")
        print("✓ La red es valida")

main()