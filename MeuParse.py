#Autor 1: Nycolas Felipe de Oliveira, 20161120961
#Autor 2: Matheus Bomfim F. Fonseca, 20161101011

import sys
from MeuLex import *

# O objeto analisador Sintático rastreia o token atual, verifica se o código corresponde à gramática e emite código ao longo do caminho.
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()    # Todas as variáveis que declaramos até agora.
        self.labelsDeclared = set() # Mantem o controle de todos os rotulos. 
        self.labelsGotoed = set() # Todos os rótulos foram acessados, então sabemos se eles existem ou não.

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Chame pela segunda vez para inicializar o peek atual.

    # Retorna VERDADEIRO se o token atual corresponder.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Retorna VERDADEIRO se o próximo token corresponder.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Tente combinar o token atual, caso contrário informa erro. Avança o token atual.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Esperado " + kind.name + ", Encontrado " + self.curToken.kind.name)
        self.nextToken()

    # Avança o token atual.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # Não precisa se preocupar em passar o EOF, o lexer cuida disso.

    # Retorna VERDADEIRO se o token atual for um operador de comparação.
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)

    def abort(self, message):
        sys.exit("Erro! " + message)


    # Regras de produção.

    # Programa ::= {declaração}
    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")
        
        # Uma vez que algumas novas linhas são necessárias em nossa gramática, é necessário pular o excesso.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Analisa todas as instruções do programa.
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # Embrulha 
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        # Verifica se cada rótulo referenciado em um GOTO está declarado.
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Tentando encontrar um label não declarado: " + label)


    # Uma das seguintes afirmações ...
    def statement(self):
        # Verifica o primeiro token para ver que tipo de declaração é.

        # "PRINT" (expressão | fragmento)
        if self.checkToken(TokenType.PRINT):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # String simples, imprima.
                self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
                self.nextToken()

            else:
                # Espera uma expressão e imprima o resultado como um float.
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

        # "IF" comparação "THEN" bloqueia "ENDIF"
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")

            # Zero ou mais declarações no corpo.
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")

        # "WHILE" comparação "REPEAT" bloqueia "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")

            # Zero ou mais instruções no corpo do loop.
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            self.nextToken()

            # Certifca de que este rótulo ainda não exista.
            if self.curToken.text in self.labelsDeclared:
                self.abort("A Label já existe: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emitLine(self.curToken.text + ":")
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emitLine("goto " + self.curToken.text + ";")
            self.match(TokenType.IDENT)

        # "LET" ident = expression
        elif self.checkToken(TokenType.LET):
            self.nextToken()

            #  Verifique se existe ident na tabela de símbolos. Se não, declare.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            
            self.expression()
            self.emitter.emitLine(";")

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            self.nextToken()

            # Se a variável ainda não existe, declare-a.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            # Emita scanf, mas também valide a entrada. Se inválido, defina a variável como 0 e limpe a entrada.
            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
            self.emitter.emitLine(self.curToken.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.IDENT)

        # Se não é uma declaração válida. Erro!
        else:
            self.abort("Declaração Invalida em " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Nova linha.
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        self.expression()

        # Deve haver pelo menos um operador de comparação e outra expressão.
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        # Pode ter 0 ou mais operadores e expressões de comparação.
        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()


    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        self.term()
        # Pode ter 0 ou mais +/- e expressões.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()


    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        self.unary()
        # Pode ter 0 ou mais * // e expressões.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()


    # unary ::= ["+" | "-"] primary
    def unary(self):
        # Unário opcional +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()        
        self.primary()


    # primary ::= number | ident
    def primary(self):
        if self.checkToken(TokenType.NUMBER): 
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Certifique-se de que a variável já existe.
            if self.curToken.text not in self.symbols:
                self.abort("Referenciando uma variavel não incializada: " + self.curToken.text)

            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort("Token Inesperado em: " + self.curToken.text)

    # nl ::= '\n'+
    def nl(self):
        # Requer pelo menos uma nova linha.
        self.match(TokenType.NEWLINE)
        # Mas permitiremos novas linhas extras também, é claro.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
