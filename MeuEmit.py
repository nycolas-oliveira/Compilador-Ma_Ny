#Autor 1: Nycolas Felipe de Oliveira, 20161120961
#Autor 2: Matheus Bomfim F. Fonseca, 20161101011

# O objeto Emitter mantém o controle do código e faz a geração do arquivo de saida.
class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emitLine(self, code):
        self.code += code + '\n'

    def headerLine(self, code):
        self.header += code + '\n'

    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)
