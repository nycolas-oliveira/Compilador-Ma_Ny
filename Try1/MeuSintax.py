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

def p_program(t):
    'program : sequencia_declaracoes'

    t[0]=t[1]


def p_sequencia_declaracoes(t):
    '''sequencia_declaracoes : declaracoes sequencia_declaracoes
                             | declaracoes'''

    t[0]=var_global


def p_declaracoes(t):
    '''declaracoes  : var_Declaracoes'''
    t[0]=t[1]

def p_var_declaracoes(t):
    '''var_Declaracoes : type sequence_var_Especificacoes end'''
    tmp=t[2]
    for element in tmp:
        tmp[element].def_type(t[1])
        var_global.add(tmp[element])
    t[0]=tmp

def p_list_var_declaracoes(t):
    '''list_var_Declaracoes : var_Declaracoes list_var_Declaracoes
                            | empty'''
    global var_global
    if(len(t)>2):
        if(t[2] is not None):
            tmp=t[1]
            tmp.update(t[2])
            t[0]=tmp
        else:
            t[0]=t[1]

def p_var_especificacoes(t):
    '''var_Especificacoes   : NOME RECEBE expressao
                            | NOME'''
    if(len(t)==2):
        t[0]=Variable(t[1], None, None)

    elif(len(t)==4):
        t[0]=Variable(t[1], None, t[3])



def p_sequencia_var_Especificacoes(t):
    '''sequencia_var_Especificacoes  : var_Especificacoes VIRGULA sequencia_var_Especificacoes
                                     | var_Especificacoes'''
    if len(t)<4:
        tmp={}
    else:
        tmp=t[3]
    tmp[t[1].nome]=t[1]
    t[0]=tmp



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