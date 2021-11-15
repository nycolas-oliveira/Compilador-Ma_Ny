#Autor 1: Nycolas Felipe de Oliveira
#Autor 2: Matheus Bomfim

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

import sys
sys.path.append("../..")

import MeuSintax
import erros

show = False
if len(sys.argv) < 2:
    print("uso : many [-show] arquivodeentrada")
    raise SystemExit

if len(sys.argv) == 3: 
    if sys.argv[1] == '-show':
        show = True; 
    else:
        print("Opção Desconhecida '%s'" % sys.argv[1])
        raise SystemExit 
    
    nomearquivo = sys.argv[2]
else: 
    nomearquivo = sys.argv[1]

arquivo = open(nomearquivo).read()

MeuSintax.parser.parse(arquivo)

if show: 
    print(MeuSintax.var_global) 