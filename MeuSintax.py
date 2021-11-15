#Autor 1: Nycolas Felipe de Oliveira
#Autor 2: Matheus Bomfim

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-


#Manipulação de Arquivos
import sys
sys.path.append("../..")


import ply.yacc as yacc
import erros
import declaracoes
from declaracoes import *
from MeuLexer import tokens
import MeuLexer

if "many" not in sys.argv[1]: 
    print("uso : many arquivodeentrada")
    raise SystemExit

GLOBAL = "GLOBAL"
TMP="TMP"


var_global = Escopo(GLOBAL)



precedence = (
    ('left', 'DPAREN', 'EPAREN'), 
    ('left', 'E', 'OU'), 
    ('left', 'IGUAL', 'MENOR', 'MAIOR'),
    ('left', 'SOMA', 'SUBTRAI'), 
    ('left', 'MULTIPLICA', 'DIVIDE'),

)

def p_vazio(p):
    'empty :'
    pass

def fim_de_instrucao(p):
     'end : PONTOVIRGULA'


# def p_variavel(t):
#     '''variavel : NOME
#                 | NOME EPAREN expressao DPAREN'''
#     t[0] = t[1]

# def p_program(t):
#     'program : sequencia_declaracoes'

#     t[0]=t[1]


# def p_sequencia_declaracoes(t):
#     '''sequencia_declaracoes : declaracoes sequencia_declaracoes
#                              | declaracoes'''

#     t[0]=var_global


def p_expressao(p): 
    'expressao : EPAREN expressao DPAREN'
    p[0] = p[2]


def p_expressao_logop(t):
    '''expressao : expressao MAIOR expressao
                 | expressao MENOR expressao
                 | expressao IGUAL expressao
                 | expressao E expressao
                 | expressao OU expressao'''
    
    if t[2] == '>'  : t[0] = t[1] > t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]
    elif t[2] == '=': t[0] = t[1] == t[3]
    elif t[2] == '|E': t[0] = t[1] and t[3]
    elif t[2] == '|OU': t[0] = t[1] or t[3]
    else: erros.unknownSignal(t)

def p_lista_expressoes(t):
    '''lista_expressoes : sequencia_expressoes
                        | empty'''
    t[0]=t[1]

def p_sequencia_expressoes(t):
    '''sequencia_expressoes : expressoes PONTOVIRGULA sequencia_expressoes
                            | expressoes'''

    t[0] = [t[1]] + t[3] if(len(t)>2) else [t[1]]


def p_operadores(p):
    '''expressao : expressao SOMA expressao
                 | expressao SUBTRAI expressao
                 | expressao MULTIPLICA expressao
                 | expressao DIVIDE expressao'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    else: erros.unknownSignal(p)


def p_statement(t):
    '''statement : escreva_statement end
                 | leia_statement end'''
        
    t[0]=t[1]

def pstatement_escreva(t):
    '''escreva statement : ESCREVA lista_expressoes'''
    tmp=""
    for element in t[2]:
        tmp+=str(element)+" "
        print("Na Execução: "+tmp)


def p_error(t):
    parser.errok()
    erros.unknownError(t)


parser = yacc.yacc(start='program')