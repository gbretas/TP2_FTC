from tqdm import tqdm


# CYK Original

# input: a CFG G = (N,Σ,S,→) in CNF, a word w = a1...an ∈ Σ+
 
# CYK(G,w) =
# 1     for i=1,...,n do
# 2        Ti,i : = {A ∈ N | A→ ai}
# 3     for j=2,...,n do
# 4        for i=j-1,...,1 do
# 5            Ti,j : = ∅;
# 6            for h=i,...,j-1 do
# 7                for all A → BC
# 8                    if B ∈ Ti,h and C ∈ Th+1,j then
# 9                       Ti,j : = Ti,j ∪{ A }
 
# 10    if S ∈ T1,n then return yes else return no
 

# Figure 1: Algorithm CYK for the word problem of CFGs in CNF.


def cyk(gram, word):

    # 1. Inicializar a tabela
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1
    table = [[[] for i in range(n)] for j in range(n)]

    # 2. Preencher a tabela

    interation = 0
    for j in range(n):
        for rule in gram.rules_dict:
            for rul in gram.rules_dict[rule]:
                interation += 1
                # print("Interation: {} of {}".format(interation, maxInterations))
                if len(rul) == 1:
                    if rul == word[j]:
                        table[j][j].append(rule)


    desc = "`{}` aceita? (running) ".format(word)
    tqdmProgress = tqdm(desc=desc, unit=" interations", ncols=100)

    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            for k in range(i, j):
                for rule in gram.rules_dict:
                    for rul in gram.rules_dict[rule]:
                        tqdmProgress.update(1)
                        if len(rul) == 2:
                            for a in table[i][k]:
                                for b in table[k+1][j]:
                                    if rul == a + b:
                                        table[i][j].append(rule)

    tqdmProgress.set_description_str("`{}` aceita? {}".format(word, gram.start in table[0][n-1]))
    tqdmProgress.close()
    # tqdmProgress.close()

    # 3. Verificar se a palavra é gerada pela gramática
    # if accept λ

    

    if gram.start in table[0][n-1]:
        return True
    else:
        return False