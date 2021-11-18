#Autor 1: Nycolas Felipe de Oliveira, 20161120961
#Autor 2: Matheus Bomfim F. Fonseca, 20161101011


from typing import SupportsAbs
from MeuLex import *
from MeuEmit import *
from MeuParse import *
from auxfunc import executaArq
from time import sleep
import sys


def main():
    print("===>Compilador MaNy<===")

    if len(sys.argv) != 2:
        sys.exit("->Erro: O compilador precisa de um arquivo de entrada como argumento.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    # Inicializando o lexer, emitter e parser.
    lexer = Lexer(input)
    emitter = Emitter("./temp/Saida.c")
    parser = Parser(lexer, emitter)

    parser.program() # Iniciando o parser.
    emitter.writeFile() # Escrevendo o arquivo de saida.
    print("->Compilação Completa.")
    sleep(1)
    print("->Executando")
    executaArq()

main()