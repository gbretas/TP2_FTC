# Fundamentos Teóricos da Computação
# Trabalho Prático 2
# Implementação do algoritmo CYK e CYK-M
# Gustavo Torres Bretas Alves - 689655
# Maria Fernanda Oliveira Guimarães - 690667

import os
import time
from resources.grammar import Grammar
from resources.converts import convertToChomsky, convertTo2NF
from resources.cyk import cyk
from resources.cykm import cyk_for_2nf



def ler_entrada(arquivo):
    """
    Lê o arquivo de entrada e retorna uma gramática e uma lista de entradas
    """

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
        try:
            rule = splitted[0]
            rul = splitted[1].split("|")
        except:
            # throw error
            raise Exception("Erro ao ler arquivo de entrada")

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


def selectEntrada():
    """
    Seleciona o arquivo de entrada
    """
    # folder inputs
    allFiles  = os.listdir("inputs")
    indices = []
    for file in allFiles:
        if file.endswith(".txt"):
            indices.append(file)

    # order indices
    indices.sort()

    # print indices
    for i in range(len(indices)):
        print("{} - {}".format(i+1, indices[i]))

    entrada = int(input("Escolha o arquivo de entrada (ex.: 1): "))

    if entrada > len(indices) or entrada < 1:
        print("Entrada inválida")
        return None

    return "inputs/" + indices[entrada - 1]


def teste_cyk(gramatica, entradas):
    """
    Testa o algoritmo CYK-Original
    """

    start_time = time.time()
    gramatica_chom = convertToChomsky(gramatica)
    end_time = time.time()

    # tempo_conversao_cyk in ms
    tempo_conversao_cyk = (end_time - start_time) * 1000

    # print("Gramática em Chomsky: \n {}".format(gramatica_chom))
  

    start_time = time.time()
    print("CYK-Original")
    for entrada in entradas:
        validacao = cyk(gramatica_chom, entrada)
    print("")

    end_time = time.time()

    # tempo_cyk in ms
    tempo_execucao_cyk = (end_time - start_time) * 1000
    
    tempo_conversao_cyk = round(tempo_conversao_cyk, 2)
    tempo_execucao_cyk = round(tempo_execucao_cyk, 2)


    return tempo_conversao_cyk, tempo_execucao_cyk

def teste_cyk_m(gramatica, entradas):
    """
    Testa o algoritmo CYK-M
    """

    start_time = time.time()
    gramatica_2nf = convertTo2NF(gramatica)
    end_time = time.time()

    tempo_conversao_cyk_m = (end_time - start_time) * 1000


    print("É 2NF? {}".format(gramatica_2nf.is_2nf()))

    start_time = time.time()
    print("2NF: ")
    for entrada in entradas:
        validacao = cyk_for_2nf(gramatica_2nf, entrada)

    print("")
    end_time = time.time()

    tempo_execucao_cyk_m = (end_time - start_time) * 1000

    tempo_conversao_cyk_m = round(tempo_conversao_cyk_m, 2)
    tempo_execucao_cyk_m = round(tempo_execucao_cyk_m, 2)

    return tempo_conversao_cyk_m, tempo_execucao_cyk_m
