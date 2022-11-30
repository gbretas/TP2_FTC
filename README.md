# CYK e CYK Modificado

Trabalho desenvolvido em **Python** para a disciplina de Teoria da Computação, ministrada pelo professor Zenilton, no curso de Ciência da Computação da PUC Minas.

------

## Alunos

Gustavo Torres Bretas Alves - 689655 \
Maria Fernanda Oliveira Guimarães - 690667Print2022-11-30 at 12.18.17@2x.jpg

------
## Execução

Para executar o programa, basta executar o arquivo **main.py** usando:
````
python main.py
````
O programa irá pedir o index do arquivo de entrada, que deve estar na pasta **inputs**.\
O arquivo de entrada deve estar no formato descrito abaixo.

Tenha certeza de que está na pasta raiz do projeto, pois o programa irá procurar os arquivos de entrada na pasta **inputs**.

### Exemplo de execução

````
(base) gbretas@macprom1 TP2 % python3 main.py
1 - entrada01.txt
2 - entrada02.txt
3 - entrada03.txt
4 - entrada04.txt
5 - entrada05.txt
6 - entrada06.txt
7 - entrada07.txt
8 - readme.txt
Escolha o arquivo de entrada (ex.: 1): 2

CYK-Original
`00` aceita? True: 17 interations [00:00, 61841.43 interations/s] 
`011` aceita? False: 68 interations [00:00, 352114.41 interations/s]
`000` aceita? True: 68 interations [00:00, 450572.94 interations/s]
`0000` aceita? True: 170 interations [00:00, 596679.23 interations/s]
`00000` aceita? True: 340 interations [00:00, 649983.30 interations/s]
`101101` aceita? True: 595 interations [00:00, 864730.03 interations/s]
`101101101101101101101101101101101101101101` aceita? True: 209797 interations [00:00, 1075456.39 interations/s]    
`101101101101101101101101101101101101101101101101101101101101` aceita? True: 611830 interations [00:00, 1141320.03 interations/s]      
`101101101101101101111101101101101101101101101101101101101101` aceita? False: 611830 interations [00:00, 1214539.17 interations/s]     

É 2NF? True
2NF: 
`00` aceita? True: 7 interations [00:00, 88701.29 interations/s] 
`011` aceita? False: 28 interations [00:00, 304250.03 interations/s]
`000` aceita? True: 28 interations [00:00, 310689.19 interations/s]
`0000` aceita? True: 70 interations [00:00, 542701.07 interations/s]
`00000` aceita? True: 140 interations [00:00, 724941.43 interations/s]
`101101` aceita? True: 245 interations [00:00, 878294.43 interations/s] 
`101101101101101101101101101101101101101101` aceita? True: 86387 interations [00:00, 968930.08 interations/s]
`101101101101101101101101101101101101101101101101101101101101` aceita? True: 251930 interations [00:00, 1161535.60 interations/s]      
`101101101101101101111101101101101101101101101101101101101101` aceita? False: 251930 interations [00:00, 1220739.63 interations/s]     

Tempo CYK: 1.26s
Tempo CYK-Modificado: 0.52s

Deseja executar outro arquivo de entrada?
1. Sim
2. Não
Opção: 2
Saindo...

````



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

------

## Estrutura de arquivos

```
.
├── README.md
├── inputs
│   ├── entrada01.txt
│   ├── entrada02.txt
│   ├── entrada03.txt
│   ├── entrada04.txt
│   ├── entrada05.txt
│   ├── entrada06.txt
│   ├── entrada07.txt
│   └── readme.txt
├── main.py
└── resources
    ├── converts.py
    ├── cyk.py
    ├── cykm.py
    ├── functions.py
    ├── grammar.py

```

README.md: Arquivo que contém a descrição do trabalho.\
inputs: Pasta que contém os arquivos de entrada.\
main.py: Arquivo que contém o código principal.\
resources: Pasta que contém os arquivos de recursos.\
    - converts.py: Arquivo que contém as funções de conversão de gramáticas.\
    - cyk.py: Arquivo que contém as funções de CYK.\
    - cykm.py: Arquivo que contém as funções de CYK Modificado.\
    - functions.py: Arquivo que contém as funções auxiliares.\
    - grammar.py: Arquivo que contém a classe Gramática.

----

## Referências

Materiais de aula

https://www.youtube.com/watch?v=VTH1k-xiswM&pp=ugMICgJwdBABGAE%3D

https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en

https://github.com/Kymberlly/CYK_Modificado/

https://github.com/nikoladimitroff/CfgSolver/

