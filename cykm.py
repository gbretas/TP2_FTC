from tqdm import tqdm
from printTable import printTable

# CYK Modificado
# 	    CYK(G,ÛG,w) =
# 1    for i=1,...,n do
# 2       Ti,i : = Û*G({ai})
# 3       for j=2,...,n do
# 4           for i=j-1,...,1 do
# 5                  T2 i,j : = ∅
# 6                  for h=i,...,j-1 do
# 7                      for all A → yz
# 8                          if y ∈ Ti,h and z ∈ Th+1,j then
# 9                              T2 i,j : = T2 i,j ∪{ A }
# 10               Ti,j : = Û*G(T2 i,j)
# 11       if S ∈ T1,n then return yes else return no
def cyk_for_2nf(gram, word):

    n = len(word)
    if n == 0:
        word = "λ"
        n = 1

    # 1. Inicializar a tabela
    table = [[[] for i in range(n)] for j in range(n)]

    # 2. Preencher a tabela

    for i in range(n):
        states = [gram.start]
        # for alcancaveis in gram.reachableFromWithSymbol(gram.start, word[i]):
        #     table[i][i].append(alcancaveis)
        for state in states:
            for alcancaveis in gram.reachableFromWithSymbol(state, word[i]):
                for rul in gram.rules_dict[alcancaveis]:
                    if alcancaveis not in table[i][i]:
                        table[i][i].append(alcancaveis)
                # states.append(alcancaveis)


    desc = "`{}` aceita? (running) ".format(word)
    tqdmProgress = tqdm(desc=desc, unit=" interations", ncols=100)

    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            for k in range(i, j):
                for rule in gram.rules_dict:
                    for rul2 in gram.reachableFrom(rule):
                        for rul in gram.rules_dict[rul2]:
                            tqdmProgress.update(1)

                            if len (rul) == 2:
                                for a in table[i][k]:
                                    for b in table[k+1][j]:
                                        if b in rul and a in rul:
                                            # print("rul: {} a: {} b: {}".format(rul, a, b))

                                            if rule not in table[i][j]:
                                                table[i][j].append(rule)

                            elif len(rul) == 1:
                                for a in table[i][k]:
                                    for b in table[k+1][j]:
                                        if b in rul and a in rul:
                                            # print("rul: {} a: {} b: {}".format(rul, a, b))

                                            if rule not in table[i][j]:
                                                table[i][j].append(rule)
                       


    tqdmProgress.set_description_str("`{}` aceita? {}".format(word, gram.start in table[0][n-1]))
    tqdmProgress.close()


    # print("")
    # print("start: " +gram.start)
    # # table[0][n-1] = "kk"
    # printTable(table)
    # print(gram.start + " in table[0][n-1]: " + str(gram.start in table[0][n-1]))
    # print("table[0][n-1]: "+str(table[0][n-1]))
    # print("")

    return gram.start in table[0][n-1]
