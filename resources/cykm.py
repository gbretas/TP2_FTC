from tqdm import tqdm
from resources.printTable import printTable

class Preprocessador:
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
        nullable = []
        occurs = {}

        for nonterminal in self.gram.rules_dict:
            occurs[nonterminal] = []

        for nonterminal in self.gram.rules_dict:
            for ruls in self.gram.rules_dict[nonterminal]:
                if len(ruls) == 1 and ruls in self.gram.rules_dict:
                    occurs[ruls].append(nonterminal)

        for nonterminal in self.gram.rules_dict:
            for ruls in self.gram.rules_dict[nonterminal]:
                if len(ruls) == 2 and ruls[0] in self.gram.rules_dict and ruls[1] in self.gram.rules_dict:
                    occurs[ruls[0]].append(nonterminal + ruls[1])
                    occurs[ruls[1]].append(nonterminal + ruls[0])

        todo = []
        nullable = []
        for nonterminal in self.gram.rules_dict:
            if "λ" in self.gram.rules_dict[nonterminal]:
                nullable.append(nonterminal)
                todo.append(nonterminal)

        while len(todo) != 0:
            B = todo.pop()
            for i in range(len(occurs[B])):
                if len(occurs[B][i]) == 1:
                    continue
                A = occurs[B][i][0]
                C = occurs[B][i][1]

                shouldSkip = C not in nullable or A in nullable

                if shouldSkip:
                    continue

                nullable.append(A)
                todo.append(A)

        return nullable

    # ÛG*(M) : = { x | ∃y ∈ M, (y,x) ∈ ÛG*}.
    def inverseUnitGraph(self):
        nullableSet = self.nullable()
        nonterminals = self.gram.rules_dict.keys()

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
		
    
class Reconhecedor:
    def dfs(self, graph, root):
        if root not in graph:
            return [root]

        visited = [root]
        todo = []
        for i in range(len(graph[root])):
            todo.append(graph[root][i])
            visited.append(graph[root][i])

        while len(todo) != 0:
            next = todo.pop()
            if next in graph:
                for edge in graph[next]:
                    # print(edge)
                    # print(graph["F"])
                    # print("graph[{}][{}]".format(next, edge))
                    # vertex = graph[next][0]
                    if graph[next][0] == edge:
                        vertex = graph[next][0]
                    else:
                        vertex = graph[next][1]

                    if vertex not in visited:
                        todo.append(vertex)
                        visited.append(vertex)

        return visited


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
    def alcancavel(self, graph, set):
        reachable = []
        for node in set:
            visited = self.dfs(graph, node)
            for i in range(len(visited)):
                if visited[i] not in reachable:
                    reachable.append(visited[i])

        return reachable

   
    def testarEntrada(self, grammar, graph, startSymbol, word):
        if len(word) == 0:
            return False

        table = []
        tablePrime = []
        for i in range(len(word)):
            table.append([])
            tablePrime.append([])
            for j in range(len(word)):
                table[i].append([])
                tablePrime[i].append([])

        for i in range(len(word)):
            table[i][i] = self.alcancavel(graph, [word[i]])

        desc = "`{}` aceita? (running) ".format(word)
        tqdmProgress = tqdm(desc=desc, unit=" interations", ncols=100)

        for j in range(1, len(word)):
            for i in range(j - 1, -1, -1):
                tablePrime[i][j] = []
                for h in range(i, j):
                    for nonterminal in grammar:
                        for rhs in grammar[nonterminal]:
                            tqdmProgress.update(1)

                            rule = rhs
                            condition = len(rule) == 2 and rule[0] in table[i][h] and rule[1] in table[h + 1][j]
                            if condition:
                                tablePrime[i][j].append(nonterminal)
                table[i][j] = self.alcancavel(graph, tablePrime[i][j])
                
        tqdmProgress.set_description_str("`{}` aceita? {}".format(word, startSymbol in table[0][len(word)-1]))
        tqdmProgress.close()
        return startSymbol in table[0][len(word) - 1]



def cyk_for_2nf(gram, word):
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1
        
    preprocess = Preprocessador(gram)
    inverseUnitGraph = preprocess.inverseUnitGraph()

    reconhecedor = Reconhecedor()
    reconhece = reconhecedor.testarEntrada(gram.rules_dict, inverseUnitGraph, gram.start, word)

    return reconhece
    # print(inverseUnitGraph)


    # Build a tree based in  To CNF or not to CNF? of Lange and Leiss
    # https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en
    # https://www.informaticadidactica.de/index.php?page=LangeLeiss2009_en#To_CNF_or_not_to_CNF.3F

    # // Preprocess the grammar
    # var preprocessed = CfgSolver.preprocess(grammar);
    # // Use the preprocessed grammar to validate strings
    # var word = "yourtextgoeshere";
    # var isValid = CfgSolver.recognizeWord(grammar, word);




    return
