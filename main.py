# Gustavo Torres Bretas Alves
# Maria Fernanda Oliveira Guimarães

# https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en

import os
import time
from resources.functions import *

debug = False

def executar(entrada):
    grammarInput, entradas = ler_entrada(entrada)
    # grammarInput, entradas = ler_entrada("inputs/entrada01.txt")

    print("")
    tempo_conversao_cyk, tempo_execucao_cyk = teste_cyk(grammarInput, entradas)

    tempo_conversao_cyk_m, tempo_execucao_cyk_m = teste_cyk_m(grammarInput, entradas)


    print("="*50)
    print("Métricas de desempenho")
    print("="*50)

    print("Tempo de conversão CNF: {} ms".format(tempo_conversao_cyk))
    print("Tempo de execução CYK: {} ms".format(tempo_execucao_cyk))

    print("")

    print("Tempo de conversão 2NF: {} ms".format(tempo_conversao_cyk_m))
    print("Tempo de execução CYK-M: {} ms".format(tempo_execucao_cyk_m))

    print("")

    speedupConversion = round((tempo_conversao_cyk) / tempo_conversao_cyk_m, 2)
    speedupExecution = round((tempo_execucao_cyk) / tempo_execucao_cyk_m, 2)

    print("Speedup da conversão do 2NF em relação a CNF: {}x".format(speedupConversion))
    print("Speedup da execução do CYK-M em relação CYK: {}x".format(speedupExecution))


def menu():

    selecionarEntrada = selectEntrada()
    if selecionarEntrada == None:
        print("Saindo...")
        exit()

    executar(selecionarEntrada)

    pass


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nSaindo...")
        exit()
    except Exception as e:
        print("\nErro: {}".format(e))
        exit()
# print("O tempo inclui a conversão da gramática para Chomsky/2NF, e a execução do algoritmo CYK/CYK-Modificado")