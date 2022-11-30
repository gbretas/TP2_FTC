# Gustavo Torres Bretas Alves
# Maria Fernanda Oliveira Guimarães

# https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en

import os
import time
from resources.functions import *

debug = False


grammarInput, entradas = ler_entrada("inputs/entrada05.txt")

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

# print("O tempo inclui a conversão da gramática para Chomsky/2NF, e a execução do algoritmo CYK/CYK-Modificado")