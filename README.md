# CYK e CYK Modificado

Trabalho desenvolvido em **Python** para a disciplina de Teoria da Computação, ministrada pelo professor Zenilton, no curso de Ciência da Computação da PUC Minas.

------

## Alunos

Gustavo Torres Bretas Alves - 689655 \
Maria Fernanda Oliveira Guimarães - 

------

## Objetivo
Neste trabalho, você deverá implementar **dois métodos** para verificar a **pertinência de uma sentença a uma  determinada  LLC** usando: 

**(i)  o  algoritmo  CYK  original;**\
**e  (ii)  o  algoritmo  CYK  modificado** proposto  por  Lange  e  Leiß  (2009).\
Para  tanto,  sua(s)  implementação(ões)  deve(m)  receber  como entrada um arquivo contendo a descrição de uma GLC qualquer (que não precisa estar na CNF e nem na  2FN)  juntamente  com  a(s)  sentença(s)  a  verificar  e  gerar  como  saída  outro  arquivo  contendo  o resultado da verificação. Devem ser realizados **experimentos que para avaliar o tempo médio gasto para as duas estratégias aplicadas a gramáticas de diferentes tamanhos.**

------
## Exemplo de arquivo de entrada

### Estrutura de um arquivo de entrada

```
VARIAVEL1(START),VARIAVEL2,VARIAVEL3...
TERMINAL1,TERMINAL2,TERMINAL3...
VARIAVEL:PRODUCAO1|PRODUCAO2|PRODUCAO3...
ENTRADAS
SENTENCA1
SENTENCA2
SENTENCA3...
FIM

Qualquer comentário aqui

````

### Exemplo para a GLC abaixo

G: S -> SS | () | (S) | [] | [S]

````
S
(,),[,]
S:SS|()|(S)|[]|[S]
ENTRADAS
()
()()()
()()[][]
()[[()]]
FIM
Pode-se colocar qualquer coisa aqui.
````

------

## Lógica de funcionamento

1. O usuário deve informar qual o arquivo de entrada que deseja utilizar.
2. O programa interpreta o arquivo de entrada e cria uma Grámatica, que é uma classe que contém as variáveis, terminais, produções e sentenças.
3. Teste de CYK:\
    3.1 O programa converte a Grámatica para a forma normal de Chomsky, se necessário.\
    3.2 O programa cria uma tabela CYK, que é uma classe que contém a tabela CYK e os métodos para preenchê-la, logo após, o programa preenche a tabela CYK e verifica se a sentença pertence ou não à gramática.
4. Teste de CYK Modificado:\
   4.1  O programa cria uma tabela CYK Modificado, que é uma classe que contém a tabela CYK Modificado e os métodos para preenchê-la, logo após, o programa preenche a tabela CYK Modificado e verifica se a sentença pertence ou não à gramática.

5. O programa retorna as saídas no terminal.