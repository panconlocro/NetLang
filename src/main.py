import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from antlr4 import *
from grammar.NetLangLexer import NetLangLexer
from grammar.NetLangParser import NetLangParser
from SemanticAnalyzer import SemanticAnalyzer
from IRGenerator import IRGenerator
from CodeGen import CodeGen


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/main.py <archivo.txt> [--ir] [--codegen <salida.py>]")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    emitir_ir = '--ir' in sys.argv
    archivo_salida = None
    if '--codegen' in sys.argv:
        idx = sys.argv.index('--codegen')
        if idx + 1 < len(sys.argv):
            archivo_salida = sys.argv[idx + 1]
        else:
            print("Error: --codegen requiere un nombre de archivo de salida.")
            sys.exit(1)

    # ── Fase 1: Análisis léxico y sintáctico ──────────────────────
    input_stream = FileStream(archivo_entrada, encoding='utf-8')
    lexer = NetLangLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = NetLangParser(tokens)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"✗ Se encontraron {parser.getNumberOfSyntaxErrors()} error(es) sintactico(s). Abortando.")
        sys.exit(1)

    print("✓ Analisis sintactico correcto.")

    # ── Fase 2: Análisis semántico ────────────────────────────────
    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)

    if analyzer.errors:
        print(f"✗ Se encontraron {len(analyzer.errors)} error(es) semantico(s):")
        for error in analyzer.errors:
            print(f"  - {error}")
        sys.exit(1)

    print("✓ Analisis semantico correcto.")

    # ── Fase 3: Generación de IR ──────────────────────────────────
    ir_gen = IRGenerator()
    ir_gen.visit(tree)
    network_ir = ir_gen.ir

    if emitir_ir or archivo_salida:
        llvm_ir = ir_gen.emit_llvm_ir()
        if emitir_ir:
            nombre_ir = os.path.splitext(archivo_entrada)[0] + '.ll'
            with open(nombre_ir, 'w', encoding='utf-8') as f:
                f.write(llvm_ir)
            print(f"✓ LLVM IR generado en: {nombre_ir}")

    # ── Fase 4: Generación de código Mininet ──────────────────────
    if archivo_salida:
        codegen = CodeGen(network_ir)
        script = codegen.generar()
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✓ Script Mininet generado en: {archivo_salida}")

    if not emitir_ir and not archivo_salida:
        print("Tip: usa --ir para generar LLVM IR y --codegen <salida.py> para generar el script Mininet.")

main()
