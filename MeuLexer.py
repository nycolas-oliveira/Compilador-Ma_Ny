#Autor 1: Nycolas Felipe de Oliveira
#Autor 2: Matheus Bomfim

# Incluindo caracteres especiais no programa
# -*- coding: utf-8 -*-

#Manipulação de Arquivos
import sys
sys.path.append("../..")


import string


from ply import lex

if "many" not in sys.argv[1]: 
    print("uso : many arquivodeentrada")
    raise SystemExit


reserved = {

	'boleano'	:	'BOLEANO',
	'parar'	:	'PARAR',
	'loop'	:	'LOOP',
	'falso'	:	'FALSO',
	'se'	:	'SE',
	'senao'	:	'SENAO',
	'int'	:	'INT',
	'retorne':	'RETORNE',
	'string':	'STRING',
	'verdadeiro'	:	'VERDADEIRO',
	'enquanto'	:	'ENQUANTO',
	'escreva' :	'ESCREVA',
	'leia' :	'LEIA'

}

tokens = ['NOME','NUMERO', 'SOMA', 'SUBTRAI', 'MULTIPLICA', 'DIVIDE', 'DPAREN', 'EPAREN',
'VIRGULA', 'PONTOVIRGULA', 'IGUAL', 'MENOR', 'MAIOR', 'E', 'OU', 'RECEBE']+ list(reserved.values())


t_DPAREN    = r'\)'
t_EPAREN    = r'\('
t_RECEBE    = r'\<-'

t_PONTOVIRGULA   = r'\;'
t_VIRGULA   = r'\,'
t_IGUAL     = r'\='
t_MENOR     = r'\<'
t_MAIOR     = r'\>'

t_E         = r'\|E'
t_OU        = r'\|OU'


t_SOMA      = r'\+'
t_SUBTRAI   = r'\-'
t_MULTIPLICA= r'\*'
t_DIVIDE    = r'\/'


def t_NOME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
	print("Caracter Ilegal '%s'" % t.value[0])
	t.lexer.skip(1)


if __name__ == '__main__': 
    lex.runmain()



lex.lex()