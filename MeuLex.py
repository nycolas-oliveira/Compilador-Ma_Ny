import sys
import enum

# O objeto Lexer rastreia a posição atual no código-fonte e produz cada token.
class Lexer:
    def __init__(self, input):
        self.source = input + '\n' 
        self.curChar = ''   # Caractere atual na string.
        self.curPos = -1    # Posição atual na string.
        self.nextChar()

    # Processe o próximo caractere.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Retorne o caractere.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Token inválido encontrado, imprime mensagem de erro e sai.
    def abort(self, message):
        sys.exit("Erro Lexico. " + message)

    # Retorna para o proximo token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Verificar o primeiro caracter do token.
        # Se for um operador de vários caracteres (e.g.,! =), Número, identificador ou palavra-chave, processaremos o resto.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            # Verifique se este token é = ou ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Verifique se este token é > ou >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Verifique se este token é < ou <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Esperado !=, Encontrado !" + self.peek())

        elif self.curChar == '\"':
            # Caracters entre aspas.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Não permita caracteres especiais na string. Sem caracteres de escape, novas linhas, tabulações ou %.
                # Usando printf de C nesta string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Caractere ilegal na string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] 
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            # O caractere inicial é um dígito, portanto, deve ser um número.
            # Obtem todos os dígitos consecutivos e decimais, se houver.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                self.nextChar()

                # Deve ter pelo menos um dígito após o decimal.
                if not self.peek().isdigit(): 
                    # Error!
                    self.abort("Caractere ilegal no numero.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Obtenha a substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            # O caractere inicial é uma letra, portanto, deve ser um identificador ou uma palavra-chave.
            # Obtem todos os caracteres alfanuméricos consecutivos.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Verifique se o token está na lista de palavras-chave.
            tokText = self.source[startPos : self.curPos + 1] # Obtenha a substring.
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Palavra chave.
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            # Nova linha.
            token = Token('\n', TokenType.NEWLINE)
        elif self.curChar == '\0':
             # EOF.
            token = Token('', TokenType.EOF)
        else:
            # token desconhecido 
            self.abort("Token Desconhecido: " + self.curChar)

        self.nextChar()
        return token

    # Pula os espaços em branco, exceto novas linhas.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()


# Token contém o texto original e o tipo de token.
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # Texto real do token. Usado para identificadores, strings e números.
        self.kind = tokenKind   # TokenType com o qual esse token é classificado.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Depende de todos os valores de enum de palavra-chave sendo 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# TokenType é nosso enum para todos os tipos de tokens.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Palavras chaves.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operadores.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
