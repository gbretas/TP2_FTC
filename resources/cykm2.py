from tqdm import tqdm
from resources.printTable import printTable

def cyk_for_2nf_2(gram, word):
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1

    # 1. Inicializar a tabela
    table = [[[] for i in range(n)] for j in range(n)]

    print(gram.criarFechoUnitario(word))

    

    return gram.start in table[0][n-1]
