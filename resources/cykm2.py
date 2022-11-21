from tqdm import tqdm
from resources.printTable import printTable
# public void CYKM(String palavra) {
#         String[][] T = new String[palavra.length()][palavra.length()];
#         String[][] Tt = new String[palavra.length()][palavra.length()];

#         for(int i = 0; i < palavra.length(); i++){
#             for(int j = 0; j < palavra.length(); j++){
#                 T[i][j] = "";
#                 Tt[i][j] = "";
#             }
#         }

#         for(int i = 0; i < palavra.length(); i++) {
#             //T[i][i] =  listToString(criarFechoUnitario(palavra.charAt(i)+""));
#             T[i][i] =  fechoUnitario(palavra.charAt(i)+"");
#         }

#         for(int j = 1; j <= palavra.length()-1; j++) {
#             for(int i = j-1; i >= 0; i--) {
#                 for(int h = i; h <= j-1; h++) {
#                     for (Regra r : regras) {
#                         List<String> producoes = r.getProducoes();
#                         for (String s : producoes) {
#                             if(s.length() >= 2){
#                                 String c1 = s.charAt(0) + "";
#                                 String c2 = s.charAt(1) + "";
#                                 if (T[i][h].contains(c1) && T[h + 1][j].contains(c2)) {
#                                     Tt[i][j] += r.getSimboloInicial() + " ";
#                                 }
#                         }
#                     }
#                     }
#                     T[i][j] = fechoUnitario(Tt[i][j]);
#                 }
#             }
#         }

#         for(int i = 0; i < palavra.length(); i++){
#             for(int j = 0; j < palavra.length();j++){
#                 System.out.print(T[i][j] + " ");
#             }
#             System.out.println();
#         }
#         System.out.println();
#         if((T[0][palavra.length()-1]).contains(this.simboloPartida)) {
#             System.out.println("sim");
#         }else{
#             System.out.println("nao");
#         }
#     }
def cyk_for_2nf_2(gram, word):
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1

    gram.relacaoUnitaria()

    # 1. Inicializar a tabela
    t = [[[] for i in range(n)] for j in range(n)]
    tt = [[[] for i in range(n)] for j in range(n)]

    # 2. Inicializar a diagonal principal
    for i in range(n):
        for j in range(n):
            t[i][j] = []
            tt[i][j] = []

    # 3. fechos unitarios
    for i in range(n):
        tmp = gram.fechoUnitario(word[i]+"")
        for s in tmp:
            for ss in s:
                t[i][i].append(ss)

    for j in range(1, n):
        for i in range(j-1, -1, -1):
            for h in range(i, j):
                for rule in gram.rules_dict:
                    for rul in gram.rules_dict[rule]:
                        if len(rul) >= 2:
                            c1 = rul[0]
                            c2 = rul[1]
                            if c1 in t[i][h] and c2 in t[h+1][j]:
                                tt[i][j].append(rule)
                                pass

                tmp = gram.fechoUnitario(" ".join(tt[i][j]))
                for s in tmp:
                    t[i][j].append(s)
                    pass


        

    # print(gram.criarFechoUnitario(word))

    # gram.relacaoUnitaria()
    # printTable(t)

    if gram.start in t[0][n-1]:
        print("sim")
        return True
    else:
        print("nao")
        return False


    

    return
