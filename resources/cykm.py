from tqdm import tqdm
from resources.printTable import printTable

# CYK Modificado

# input:	a CFG G = (N,Σ,S,→) in 2NF, its graph (V,ÛG),a word w = a1...an ∈ Σ+
#  	CYK(G,ÛG,w) =
#  	1    for i=1,...,n do
#  	2      Ti,i : = Û*G({ai})
#  	3      for j=2,...,n do
#  	4        for i=j-1,...,1 do
#  	5           T' i,j : = ∅
#  	6           for h=i,...,j-1 do
#  	7             for all A → yz
#  	8               if y ∈ Ti,h and z ∈ Th+1,j then
#  	9                  T' i,j : = T' i,j ∪{ A }
#  	10           Ti,j : = Û*G(T' i,j)
#  	11    if S ∈ T1,n then return yes else return no
 

# Figure 3: Algorithm CYK for the word problem of CFG in 2NF.
def cyk_for_2nf(gram, word):

    # print(gram)


    n = len(word)
    if n == 0:
        word = "λ"
        n = 1

    # 1. Inicializar a tabela
    table = [[[] for i in range(n)] for j in range(n)]
    table2 = [[[] for i in range(n)] for j in range(n)]

    # 2. Preencher a tabela

    


    # 3. Verificar se a palavra é aceita
    if gram.start in table[0][n-1]:
        print("A palavra {} é aceita pela gramática.".format(word))
        return True
    else:
        print("A palavra {} não é aceita pela gramática.".format(word))
        return False
       


    # print("")
    # print("start: " +gram.start)
    # # table[0][n-1] = "kk"
    # printTable(table)
    # print(gram.start + " in table[0][n-1]: " + str(gram.start in table[0][n-1]))
    # print("table[0][n-1]: "+str(table[0][n-1]))
    # print("")

    return gram.start in table[0][n-1]
