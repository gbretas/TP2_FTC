
from resources.grammar import Grammar
import os
from resources.converts import convertToChomsky, convertTo2NF
from resources.cyk import cyk
from resources.cykm import cyk_for_2nf
from resources.cykm2 import cyk_for_2nf_2



def ler_entrada(arquivo):
    if not os.path.isfile(arquivo):
        print("Arquivo não encontrado")
        return None

    # Abrir arquivo
    f = open(arquivo, "r")

    gramatica = Grammar()
    # Ler primeira linha
    line = f.readline()
    line = line.replace(" ", "")
    line = line.replace("\n", "")
    # A primeira linha contém as variáveis
    splitted = line.split(",")
    for var in splitted:
        if not gramatica.start:
            gramatica.start = var
        gramatica.add_variable(var)

    # Ler segunda linha
    line = f.readline()
    line = line.replace(" ", "")
    line = line.replace("\n", "")
    # A segunda linha contém os terminais
    splitted = line.split(",")
    for term in splitted:
        gramatica.add_terminal(term)

    #WHILE != ENTRADAS
    # Ler terceira linha
    line = f.readline()
    while line != "ENTRADAS\n":
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        # A terceira linha contém as regras
        splitted = line.split(":")
        rule = splitted[0]
        rul = splitted[1].split("|")

        for r in rul:
            gramatica.add_rule([rule, r])

        line = f.readline()

    #WHILE != FIM
    # Ler entradas
    entradas = []
    line = f.readline()
    # while not end of file
    while line != "FIM\n" or line != "":
        if not line:
            break
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        if line == "FIM":
            break
        entradas.append(line)

        line = f.readline()

    

    return gramatica, entradas
    
# Função para executar o CYK-Original
def teste_cyk(gramatica, entradas):
    gramatica_chom = convertToChomsky(gramatica)
    # print("Gramática em Chomsky: \n {}".format(gramatica_chom))
  

    print("CYK-Original")
    for entrada in entradas:
        validacao = cyk(gramatica_chom, entrada)
    print("")

# Função para executar o CYK-modificado
def teste_cyk_m(gramatica, entradas):
    gramatica_2nf = convertTo2NF(gramatica)

    # print("Gramática 2NF:\n {}".format(gramatica_2nf))

    # is in 2nf?
    # print("É 2NF? {}".format(gramatica_2nf.is_2nf()))

    print("2NF: ")
    for entrada in entradas:
        validacao = cyk_for_2nf_2(gramatica_2nf, entrada)
    print("")
