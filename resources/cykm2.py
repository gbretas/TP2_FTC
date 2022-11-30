from tqdm import tqdm
from resources.printTable import printTable


def cyk_for_2nf_2(gram, word):
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1



    # Build a tree based in  To CNF or not to CNF? of Lange and Leiss
    # https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en
    # https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en#To_CNF_or_not_to_CNF.3F

    # 1. Inicializar a tabela
    table = [[[] for i in range(n)] for j in range(n)]




    return
