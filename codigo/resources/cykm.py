from tqdm import tqdm   
class CYKM:
    def __init__(self, gram):
        self.gram = gram

    # input: a CFG G = (N,Σ,S,→) in 2NF
    # Nullable(G) =
    # 1    nullable : = ∅
    # 2    todo : = ∅
    # 3    for all A ∈ N do
    # 4      occurs(A) : = ∅
    # 5    for all A → B do
    # 6      occurs(B) := occurs(B) ∪{ A }
    # 7    for all A → BC do
    # 8      occurs(B) := occurs(B) ∪{ 〈A,C〉}
    # 9      occurs(C) := occurs(C) ∪{ 〈A,B 〉}
    # 10    for all A → e do
    # 11      nullable : = nullable ∪{A}
    # 12      todo : = todo ∪{A}
    # 13    while todo ≠ ∅ do
    # 14      remove some B from todo
    # 15      for all A, 〈A,C〉 ∈ occurs(B) with C ∈ nullable do
    # 16        if A ∉ nullable then
    # 17          nullable : = nullable ∪{A}
    # 18          todo : = todo ∪{A}
    # 19    return nullable

    def nullable(self):
        """
        Retorna uma lista com os não terminais que podem gerar a cadeia vazia
        """
        nullable = []
        ocorrencias = {}

        for rules in self.gram.rules_dict:
            ocorrencias[rules] = []

        for rules in self.gram.rules_dict:
            for rul in self.gram.rules_dict[rules]:
                if len(rul) == 1 and rul in self.gram.rules_dict:
                    ocorrencias[rul].append(rules)

        for rules in self.gram.rules_dict:
            for rul in self.gram.rules_dict[rules]:
                if len(rul) == 2 and rul[0] in self.gram.rules_dict and rul[1] in self.gram.rules_dict:
                    ocorrencias[rul[0]].append(rules + rul[1])
                    ocorrencias[rul[1]].append(rules + rul[0])

        todo = []
        nullable = []
        for rules in self.gram.rules_dict:
            if "λ" in self.gram.rules_dict[rules]:
                nullable.append(rules)
                todo.append(rules)

        while len(todo) != 0:
            B = todo.pop()
            for i in range(len(ocorrencias[B])):
                if len(ocorrencias[B][i]) == 1:
                    continue
                A = ocorrencias[B][i][0]
                C = ocorrencias[B][i][1]

                skip = C not in nullable or A in nullable

                if skip:
                    continue

                nullable.append(A)
                todo.append(A)

        return nullable

    # ÛG*(M) : = { x | ∃y ∈ M, (y,x) ∈ ÛG*}.
    def grafoUnitarioReverso(self):
        nullableSet = self.nullable()

        graph = {}
        addEdge = lambda left, right: graph.setdefault(left, []).append(right)

        for nonterminal in self.gram.rules_dict:
            for ruls in self.gram.rules_dict[nonterminal]:
                word = ruls
                if len(word) == 1:
                    addEdge(word, nonterminal)
                else:
                    if word[0] in nullableSet:
                        addEdge(word[1], nonterminal)
                    if word[1] in nullableSet:
                        addEdge(word[0], nonterminal)

        return graph

    def dfs(self, graph, root):
        """
        Retorna uma lista com os nós visitados em uma busca em profundidade
        """
        if root not in graph:
            return [root]

        visitados = [root]
        todo = []
        for i in range(len(graph[root])):
            todo.append(graph[root][i])
            visitados.append(graph[root][i])

        while len(todo) != 0:
            next = todo.pop()
            if next in graph:
                for edge in graph[next]:
                    if graph[next][0] == edge:
                        vertex = graph[next][0]
                    else:
                        vertex = graph[next][1]

                    if vertex not in visitados:
                        todo.append(vertex)
                        visitados.append(vertex)

        return visitados



    def alcancavel(self, graph, set):
        """
        Retorna uma lista com os nós alcançáveis a partir de um conjunto de nós
        """
        alcancaveis = []
        for node in set:
            visited = self.dfs(graph, node)
            for i in range(len(visited)):
                if visited[i] not in alcancaveis:
                    alcancaveis.append(visited[i])

        return alcancaveis


    # input:	a CFG G = (N,Σ,S,→) in 2NF, its graph (V,ÛG),a word w = a1...an ∈ Σ+
    #  	CYK(G,ÛG,w) =
    #  	1    for i=1,...,n do
    #  	2    Ti,i : = Û*G({ai})
    #  	3      for j=2,...,n do
    #  	4        for i=j-1,...,1 do
    #  	5        T' i,j : = ∅
    #  	6        for h=i,...,j-1 do
    #  	7          for all A → yz
    #  	8            if y ∈ Ti,h and z ∈ Th+1,j then
    #  	9              T' i,j : = T' i,j ∪{ A }
    #  	10        Ti,j : = Û*G(T' i,j)
    #  	11    if S ∈ T1,n then return yes else return no
    def montarTabela(self, grammar, graph, startSymbol, word):
        """
        Retorna True se a palavra é aceita pela gramática, False caso contrário
        """
        if len(word) == 0:
            return False

        table = []
        table2 = []
        for i in range(len(word)):
            table.append([])
            table2.append([])
            for j in range(len(word)):
                table[i].append([])
                table2[i].append([])

        for i in range(len(word)):
            table[i][i] = self.alcancavel(graph, [word[i]])

        desc = "`{}` aceita? (running) ".format(word)
        tqdmProgress = tqdm(desc=desc, unit=" interations", ncols=100)

        for j in range(1, len(word)):
            for i in range(j - 1, -1, -1):
                table2[i][j] = []
                for h in range(i, j):
                    for nonterminal in grammar:
                        for rhs in grammar[nonterminal]:
                            tqdmProgress.update(1)

                            rule = rhs
                            condition = len(rule) == 2 and rule[0] in table[i][h] and rule[1] in table[h + 1][j]
                            if condition:
                                table2[i][j].append(nonterminal)
                table[i][j] = self.alcancavel(graph, table2[i][j])
                
        tqdmProgress.set_description_str("`{}` aceita? {}".format(word, startSymbol in table[0][len(word)-1]))
        tqdmProgress.close()
        return startSymbol in table[0][len(word) - 1]



def cyk_for_2nf(gram, word):
    """
    Retorna True se a palavra é aceita pela gramática, False caso contrário
    """
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1


    cykm = CYKM(gram)
        
    grafoUnitarioReverso = cykm.grafoUnitarioReverso()
    reconhece = cykm.montarTabela(gram.rules_dict, grafoUnitarioReverso, gram.start, word)

    return reconhece