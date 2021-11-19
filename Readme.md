**<h1>Trabalho final, montagem do Compilador MaNy.</h1>**

Este projeto visa a criação de um compilador para a entrega de um projeto de conclusão da disciplina de Compiladores do curso de Engenharia da Computação da UVA 2021.2. 
O mesmo tem o objetivo de reconhecer uma linguagem inspirada em Basic, compilá-la e fazer a transcrição para linguagem C em um arquivo de Saída.

Autores: 

Nycolas Felipe de Oliveira, 20161120961

Matheus Bomfim F. Fonseca, 20161101011


<h2>Composição</h2>

Para a composição do compilador vamos estar utilizando as seguintes estruturas:
 
* <h3>MaNy.py</h3>

* <h3>MeuGrammar.txt</h3>

* <h3>MeuLex.py</h3>

* <h3>MeuParse.py</h3>

* <h3>MeuEmit.py</h3>


<h2>Estrutura </h2>

A estrutura de trabalho inicial pensada, e suas respectivas funcionalidades: 

**MaNy.py(main):** 

Nesta parte será realizada toda a parte de execução e chamada das funções necessárias para o funcionamento do compilador. 


**MeuLex.py:** 

No "MeuLexer" será realizada toda a parte do tratamento da analise léxica, nela será removido os espaços em branco e comentários que estejam presentes, separação dos caracteres que são reconhecidos como padrões e a criação da tabela de símbolos onde são classificados e separados os tokens. 


**MeuParse.py:** 

Nesta parte do programa vai ser realizada o tratamento das analises sintáticas. Nela é feita a separação dos símbolos presentes na linguagem, o grupo de sentença compostas dentro de uma string, o conjunto de símbolos utilizados(letras) e a gramatica empregada. 

**MeuEmit.py:** 

Nesta parte é realizada a validação de diversas regras que não pode ser realizadas nas etapas anteriores. Essa serie de validações tem como objetivo permitir que a linguagem seja transcrita para linguagem C, alem de fazer a geração do arquivo de saida.

