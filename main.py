# Gustavo Torres Bretas Alves
# Maria Fernanda Oliveira Guimarães

import sys
import os
import time
import random
from itertools import product

debug = True

# λ

# (i) o algoritmo CYK original; # FORMA NORMAL DE CHOMSKY
# (ii) o algoritmo CYK modificado # FORMA NORMAL 2NF

#  Para tanto, sua(s) implementação(ões) deve(m) receber como
# entrada um arquivo contendo a descrição de uma GLC qualquer (que não precisa estar na CNF e nem
# na 2NF) juntamente com a(s) sentença(s) a verificar e gerar como saída outro arquivo contendo o
# resultado da verificação.

# Devem ser realizados experimentos que para avaliar o tempo médio gasto para
# as duas estratégias aplicadas a gramáticas de diferentes tamanhos.

# Classe que representa uma gramática.
class Grammar:
    def __init__(self):
        self.variables = []
        self.terminals = []
        self.start = ''
        # S -> a
        # s -> B
        # S -> aB
        self.rules_dict = {}
        # S -> [a, B, aB]

    def add_variable(self, variable):
        self.variables.append(variable)

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def set_start(self, start):
        self.start = start

    def get_start(self):
        return self.start
    
    def get_rules(self, variable):
        return self.rules_dict[variable]

    def is_terminal(self, symbol):
        return symbol in self.terminals

    def is_variable(self, symbol):
        return symbol in self.variables

    # Checar se a gramática é livre de contexto.
    def is_context_free(self):
        contains_terminal = False
        for rule in self.rules_dict: # Para cada Variavel
            for rul in self.rules_dict[rule]: # Para cada regra da variavel
                rule_contains_terminal = False

                for symbol in rul: # Para cada simbolo da regra
                    if self.is_terminal(symbol):
                        contains_terminal = True

        if not contains_terminal:
            return False

        return True

    # Checar se a gramática é na forma normal de Chomsky.
    # A -> BC | a
    def is_chomsky(self):
        for rule in self.rules_dict: # Para cada Variavel
            for rul in self.rules_dict[rule]: # Para cada regra da variavel

                # Verificar regras de choomsky
                if rule == self.start and len(rul) == 1 and rul == "λ":
                    continue
                elif len(rul) == 1 and self.is_terminal(rul[0]):
                    continue
                elif len(rul) == 2 and self.is_variable(rul[0]) and self.is_variable(rul[1]):
                    continue
                else:
                    return False

        return True
               
    
    # Checar se a gramática é na forma normal 2NF.
    # len(rule) <= 2
    def is_2nf(self):
        for rule in self.rules_dict: # Para cada Variavel
            for rul in self.rules_dict[rule]: # Para cada regra da variavel
                if len(rul) > 2:
                    return False

        return True

    def have_lambda(self):
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                if rul == "λ" and rule != self.start:
                    return True
        return False

    def have_unitary(self):
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                if len(rul) == 1 and rul != "λ" and self.is_variable(rul):
                    return True
        return False

    def add_rule(self, rule):
        if rule[0] not in self.rules_dict:
            self.rules_dict[rule[0]] = []
            for rul in rule[1::]:
                self.rules_dict[rule[0]].append(rul)
        else:
            for rul in rule[1::]:
                if rul not in self.rules_dict[rule[0]]:
                    self.rules_dict[rule[0]].append(rul)

    def copy(self):
        grammar = Grammar()
        grammar.variables = self.variables.copy()
        grammar.terminals = self.terminals.copy()
        grammar.start = self.start
        grammar.rules_dict = self.rules_dict.copy()
        return grammar

    def __str__(self):

        regras_formatadas = "\n"
        for rule in self.rules_dict:
            regras_formatadas += "  "+rule + " -> "
            for rul in self.rules_dict[rule]:
                regras_formatadas += rul + " | "
            regras_formatadas = regras_formatadas[:-3]
            regras_formatadas += "\n"
            

        return 'Variáveis: {}\nTerminais: {}\nInício: {}\nRegras: {}'.format(self.variables, self.terminals, self.start, regras_formatadas)

    def __repr__(self):
        return self.__str__()

# Função que pega a próxima letra do alfabeto.
def getNextAlphabet(gram):
    nextAlpha = chr(ord('A') + len(gram.variables))
    while nextAlpha in gram.variables:
        nextAlpha = chr(ord(nextAlpha) + 1)

    return nextAlpha


# Função para gerar combinações possíveis de trocas.
def filler(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))

# Converter uma grámatica para a forma normal de Chomsky.
def convertToChomsky(gram):
    if gram.is_chomsky():
        return gram

    new_gram = Grammar()
    new_gram.variables = gram.variables
    new_gram.terminals = gram.terminals
    
    # 1 Introduzir nova variável de partida
    if debug:
        print("1. Introduzir nova variável de partida")
    new_gram.start = getNextAlphabet(new_gram)

    new_gram.set_start(new_gram.start)
    new_gram.add_variable(new_gram.start)
    new_gram.add_rule([new_gram.start, gram.start])

    # copy all rules
    for rule in gram.rules_dict:
        for rul in gram.rules_dict[rule]:
            new_gram.add_rule([rule, rul])



    # 2 Remover λ-produções
    # while gram.have_lambda():
    if debug:
        print("2. Removendo λ-produções\n")
    # for range
    removeds = []
    while new_gram.have_lambda():
    
        for rule in new_gram.rules_dict: # Para cada Variavel
            for rul in new_gram.rules_dict[rule]: # Para cada regra da variavel
                if rul == "λ":
                    # Remover as regras
                    if debug:
                        print("Removendo regra: {} -> {}".format(rule, rul))


                    try:
                        # if is start
                        if rule != new_gram.start:
                            new_gram.rules_dict[rule].remove(rul)
                            removeds.append([rule, rul])
                    except:
                        pass

                    # Adicionar regras
                    for rule2 in new_gram.rules_dict:
                        for rul2 in new_gram.rules_dict[rule2]:

                            # ocurrencies of rule in rul2
                            ocurrencies = 0
                            for symbol in rul2:
                                
                                if symbol == rule:
                                    ocurrencies += 1

                            if ocurrencies == 1:    
                                changed = rul2.replace(rule, "λ")

                                if changed != "λ":
                                    changed = changed.replace("λ", "")

                                if changed != rul2:
                                    
                                    if [rule2, changed] not in removeds:
                                        if debug:
                                            print("     Adicionando regra: {} -> {}".format(rule2, changed))
                                        new_gram.add_rule([rule2, changed])
                            elif ocurrencies > 1:
                                # Combinações = occurencies + 1
                                # print("     Maior")
                                # print("     Occurrencies of {} in {} is {}".format(rule, rul2, ocurrencies))
                                # new_gram.add_rule([rule2, rul2])

                                # all possible combinations to replace rule to λ in rul2
                                combinations = list(filler(rul2, rule, "λ"))
                                for combination in combinations:
                                    if combination != "λ":
                                        combination = combination.replace("λ", "")
                                    if [rule2, combination] not in removeds:
                                        if debug:
                                            print("     Adicionando regra: {} -> {}".format(rule2, combination))
                                        new_gram.add_rule([rule2, combination])

                                

                    
                    if debug:
                        print("\n")
                    pass
    if debug:
        print("Regras removidas: {}\n".format(removeds))
    # 3 Remover produções unitárias
    if debug:
        print("3. Removendo produções unitárias de variáveis\n")

    # Remover variavel que deriva ela mesma
    for rule in new_gram.rules_dict:
        for rul in new_gram.rules_dict[rule]:
            if rule == rul:
                new_gram.rules_dict[rule].remove(rul)
                pass


    while new_gram.have_unitary():
        for rule in new_gram.rules_dict:
            for rul in new_gram.rules_dict[rule]:
                # print(rule, rul)
                if len(rul) == 1 and rul != "λ" and new_gram.is_variable(rul):
                    if debug:
                        print("Removendo regra: {} -> {}".format(rule, rul))
                    # Rule -> rul
                    new_gram.rules_dict[rule].remove(rul)
                    removeds.append([rule, rul])
                    # adicionar todas as regras do rul para o rule
                    if debug:
                        print("Adicionando regras: ")
                    for rule2 in new_gram.rules_dict:
                        for rul2 in new_gram.rules_dict[rule2]:
                            if rule2 == rul:
                                if debug:
                                    print("     {} -> {}".format(rule, rul2))
                                new_gram.add_rule([rule, rul2])


    if debug:
        print("")
    # 4 Converte regras remanescentes

    if debug:
        print("4. Converte regras remanescentes\n")

    while not new_gram.is_chomsky():
    # for i in range(0, 0):


        # Tratamos os vt OU tv
        for rule in list(new_gram.rules_dict):
            for rul in new_gram.rules_dict[rule]:
                if len(rul) == 2:
                    # check if is one variable and one terminal
                    terminalTmp = False
                    if (new_gram.is_variable(rul[0]) and new_gram.is_terminal(rul[1])):
                        terminalTmp = rul[1]
                    elif (new_gram.is_variable(rul[1]) and new_gram.is_terminal(rul[0])):
                        terminalTmp = rul[0]

                    if terminalTmp:
                        # verificar se existe alguma regra que gera somente o terminal
                        gerador = False
                        for rule2 in new_gram.rules_dict:
                            rulesInRule2 = len(new_gram.rules_dict[rule2])
                            if rulesInRule2 == 1:
                                if new_gram.rules_dict[rule2][0] == terminalTmp:
                                    gerador = rule2
                                    break
                        
                        if not gerador:
                            gerador = getNextAlphabet(new_gram)

                            new_gram.add_variable(gerador)
                            new_gram.add_rule([gerador, terminalTmp])

                        

                        if gerador:
                            if debug:
                                print("Removendo regra: {} -> {}".format(rule, rul))
                            # replace terminal to gerador in rule
                            new_gram.rules_dict[rule].remove(rul)
                            rulTmp = rul.replace(terminalTmp, gerador)

                            new_gram.add_rule([rule, rulTmp])

        # tratar os tt
        for rule in list(new_gram.rules_dict):
            for rul in new_gram.rules_dict[rule]:
                if len(rul) == 2:
                    # check if is two terminals
                    if (new_gram.is_terminal(rul[0]) and new_gram.is_terminal(rul[1])):
                        # replace terminal to gerador in rule
                        new_gram.rules_dict[rule].remove(rul)
                        
                        first = rul[0]
                        second = rul[1]

                        # check if exists a rule that generates first
                        gerador = False
                        for rule2 in new_gram.rules_dict:
                            rulesInRule2 = len(new_gram.rules_dict[rule2])
                            if rulesInRule2 == 1:
                                if new_gram.rules_dict[rule2][0] == first:
                                    gerador = rule2
                                    break

                        if not gerador:
                            gerador = getNextAlphabet(new_gram)

                            new_gram.add_variable(gerador)
                            new_gram.add_rule([gerador, first])

                        if gerador:
                            if debug:
                                print("Removendo regra: {} -> {}".format(rule, rul))
                            # new_gram.rules_dict[rule].remove(rul)
                            rulTmp = rul.replace(first, gerador)

                            new_gram.add_rule([rule, rulTmp])

                        
                        # check if exists a rule that generates second
                        gerador = False
                        for rule2 in new_gram.rules_dict:
                            rulesInRule2 = len(new_gram.rules_dict[rule2])
                            if rulesInRule2 == 1:
                                if new_gram.rules_dict[rule2][0] == second:
                                    gerador = rule2
                                    break

                        if not gerador:
                            gerador = getNextAlphabet(new_gram)

                            new_gram.add_variable(gerador)
                            new_gram.add_rule([gerador, second])

                        if gerador:
                            if debug:
                                print("Removendo regra: {} -> {}".format(rule, rul))
                            # new_gram.rules_dict[rule].remove(rul)
                            rulTmp = rul.replace(second, gerador)

                            new_gram.add_rule([rule, rulTmp])



        if debug:  
            print("\n4.2")

        print(new_gram)
        for rule in list(new_gram.rules_dict):
            for rul in new_gram.rules_dict[rule]:
                if len(rul) > 2:
                    # if all symbols are variables
                    for symbol in rul:
                        if not new_gram.is_variable(symbol):
                            break
                    print("Removendo regra: {} -> {}".format(rule, rul))
                    # two first symbols
                    twoFirst = rul[:2]

                    gerador = False
                    for rule2 in new_gram.rules_dict:
                        rulesInRule2 = len(new_gram.rules_dict[rule2])
                        if rulesInRule2 == 1:
                            if new_gram.rules_dict[rule2][0] == twoFirst:
                                gerador = rule2
                                break
                    
                    if not gerador:
                        gerador = getNextAlphabet(new_gram)
    
                        new_gram.add_variable(gerador)
                        new_gram.add_rule([gerador, twoFirst])

                    if gerador:
                        if debug:
                            print("Removendo regra: {} -> {}".format(rule, rul))
                        # replace terminal to gerador in rule
                        new_gram.rules_dict[rule].remove(rul)
                        rulTmp = rul.replace(twoFirst, gerador)

                        new_gram.add_rule([rule, rulTmp])

        removed_vars = []    

            


    if debug:
        print("="*50)
        print("")



    return new_gram

# Converter gramática para 2NF
def convertTo2NF(gram):
    if gram.is_2nf():
        return gram

    new_gram = gram.copy()

    # 1 Remover variáveis inúteis
    # if debug:
    #     print("1. Removendo variáveis inúteis\n")

    # Remover variavel que deriva ela mesma
    # for rule in new_gram.rules_dict:
    #     for rul in new_gram.rules_dict[rule]:
    #         if rule == rul:
    #             new_gram.rules_dict[rule].remove(rul)
    #             pass


    for rule in list(new_gram.rules_dict):
        for rul in new_gram.rules_dict[rule]:
            if len(rul) > 2:
                if debug:
                    print("Removendo regra: {} -> {}".format(rule, rul))

                twoFirst = rul[:2]

                gerador = False
                for rule2 in new_gram.rules_dict:
                    rulesInRule2 = len(new_gram.rules_dict[rule2])
                    if rulesInRule2 == 1:
                        if new_gram.rules_dict[rule2][0] == twoFirst:
                            gerador = rule2
                            break
                
                if not gerador:
                    gerador = getNextAlphabet(new_gram)
 
                    new_gram.add_variable(gerador)
                    new_gram.add_rule([gerador, twoFirst])

                if gerador:
                    if debug:
                        print("Removendo regra: {} -> {}".format(rule, rul))
                    # replace terminal to gerador in rule
                    new_gram.rules_dict[rule].remove(rul)
                    rulTmp = rul.replace(twoFirst, gerador)

                    new_gram.add_rule([rule, rulTmp])
    
    
    
    if debug:
        print("")




    return new_gram

# CYK Original
def cyk(gram, word):
    
    if not gram.is_chomsky():
        gram = convertToChomsky(gram)

    if debug:
        print("Gramática convertida para Chomsky: ")
        print(gram)

    # 1. Inicializar a tabela
    n = len(word)
    if n == 0:
        word = "λ"
        n = 1
    table = [[[] for i in range(n)] for j in range(n)]

    # 2. Preencher a tabela
    for j in range(n):
        for rule in gram.rules_dict:
            for rul in gram.rules_dict[rule]:
                if len(rul) == 1:
                    if rul == word[j]:
                        table[j][j].append(rule)

    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            for k in range(i, j):
                for rule in gram.rules_dict:
                    for rul in gram.rules_dict[rule]:
                        if len(rul) == 2:
                            for a in table[i][k]:
                                for b in table[k+1][j]:
                                    if rul == a + b:
                                        table[i][j].append(rule)

    # print(table[0][n-1])

    # 3. Verificar se a palavra é gerada pela gramática
    # if accept λ

    

    if gram.start in table[0][n-1]:
        return True
    else:
        return False



# CREATE GRAMMAR
gramatica = Grammar()

gramatica.add_variable('S')

gramatica.add_terminal('(')
gramatica.add_terminal(')')
gramatica.add_terminal('[')
gramatica.add_terminal(']')

gramatica.set_start('S')

gramatica.add_rule(['S', 'SS', '()', '(S)', '[]', '[S]'])

print(cyk(gramatica, '()([])'))
