from MeuLex import *
from MeuEmit import *
from MeuParse import *
import sys

def main():
    print("===>Compilador MaNy<===")

    if len(sys.argv) != 2:
        sys.exit("->Erro: O compilador precisa de um arquivo de entrada como argumento.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Inicializando o lexer, emitter e parser.
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program() # Iniciando o parser.
    emitter.writeFile() # Escrevendo o arquivo de saida.
    print("->Compilação Completa.")

main()