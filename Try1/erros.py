#Autor 1: Nycolas Felipe de Oliveira
#Autor 2: Matheus Bomfim

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-


#Manipulação de Arquivos
import sys
sys.path.append("../..")

import ply.yacc as yacc


def unknownSignal(t):
    print("Sinal não reconhecido em '%s', na Linha '%d', Coluna %d!" %(t.value, t.lineno, t.lexpos))


def unknownError(t):
    if t:
         print("Erro de Syntax em '%s', na Linha %d , Coluna %d" % (t.value, t.lineno, t.lexpos))
         
    else:
         print("Erro de Syntax em EOF")
         raise SystemExit

