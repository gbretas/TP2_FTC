# Fundamentos Teóricos da Computação
# Trabalho Prático 2
# Implementação do algoritmo CYK e CYK-M
# Gustavo Torres Bretas Alves - 689655
# Maria Fernanda Oliveira Guimarães - 690667

# Códigos de referência
# https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en
# https://github.com/Kymberlly/CYK_Modificado/blob/master/src/cyk/Classes/CYK_MOD.java
# https://github.com/nikoladimitroff/CfgSolver/blob/master/cfgSolver.js

from resources.functions import *
debug = False

def executar(entrada):
    grammarInput, entradas = ler_entrada(entrada)

    print("")
    """
    Rodar os testes, retornando o tempo de conversão e execução
    """
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


if __name__ == "__main__":
    try:
        # Abrir uma entrada
        selecionarEntrada = selectEntrada()
        if selecionarEntrada == None:
            print("Saindo...")
            exit()

        executar(selecionarEntrada)
    except KeyboardInterrupt:
        print("\nSaindo...")
        exit()
    except Exception as e:
        print("\nErro: {}".format(e))
        exit()
