from antlr4 import *
from NetLangLexer import NetLangLexer
from NetLangParser import NetLangParser

input_stream = FileStream("test.nl")

lexer = NetLangLexer(input_stream)

tokens = CommonTokenStream(lexer)

parser = NetLangParser(tokens)

tree = parser.program()

print(tree.toStringTree(recog=parser))
