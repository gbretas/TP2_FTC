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
    start_time_cyk = time.time()
    teste_cyk(grammarInput, entradas)
    end_time_cyk = time.time()

    start_time_cyk_m = time.time()
    teste_cyk_m(grammarInput, entradas)
    end_time_cyk_m = time.time()

    time_cyk = round(end_time_cyk - start_time_cyk, 2)
    time_cyk_m = round(end_time_cyk_m - start_time_cyk_m, 2)

    print("Tempo CYK: {}s".format(time_cyk))
    print("Tempo CYK-Modificado: {}s".format(time_cyk_m))


def menu():

    selecionarEntrada = selectEntrada()
    if selecionarEntrada == None:
        print("Saindo...")
        exit()

    executar(selecionarEntrada)

    while True:
        print()
        print("Deseja executar outro arquivo de entrada?")
        print("1. Sim")
        print("2. Não")
        opcao = int(input("Opção: "))

        if opcao == 1:
            selecionarEntrada = selectEntrada()
            if selecionarEntrada == None:
                print("Saindo...")
                exit()

            executar(selecionarEntrada)
        elif opcao == 2:
            print("Saindo...")
            exit()
        else:
            print("Opção inválida")




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