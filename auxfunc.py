#Autor 1: Nycolas Felipe de Oliveira, 20161120961
#Autor 2: Matheus Bomfim F. Fonseca, 20161101011

from time import sleep    
import subprocess
import os


def executaArq(): 
    subprocess.call(["gcc", "./temp/Saida.c"])
    sleep(2)
    subprocess.call("a.exe")
    print("->Execução Finalizada")