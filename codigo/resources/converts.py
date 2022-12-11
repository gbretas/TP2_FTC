# Fundamentos Teóricos da Computação
# Trabalho Prático 2
# Implementação do algoritmo CYK e CYK-M
# Gustavo Torres Bretas Alves - 689655
# Maria Fernanda Oliveira Guimarães - 690667

from itertools import product
from resources.grammar import Grammar
import random
debug = False

def getNextAlphabet(gram):
    """
    Retorna o próximo caractere alfabético que não esteja sendo usado.
    """
    nextAlpha = chr(ord('A') + len(gram.variables))
    while nextAlpha in gram.variables:
        # get random alpha from A-Z
        nextAlpha = chr(ord('A') + random.randint(0, 25))

    return nextAlpha

def substituicoes(word, from_char, to_char):
    """
    Gerar todas as palavras possíveis com todas substituições de um caractere por outro.
    """
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))

def convertToChomsky(gram):
    """
    Converte uma gramática para a forma normal de Chomsky.
    Usando o método apresentado em slides da disciplina.
    """

    if gram.is_chomsky():
        # Se já estiver na forma normal de Chomsky, retorna a própria gramática
        return gram

    # 0. Criar nova gramática
    new_gram = Grammar()
    new_gram.variables = gram.variables
    new_gram.terminals = gram.terminals
    
    # 1. Introduzir nova variável de partida
    if debug:
        print("1. Introduzir nova variável de partida")
    new_gram.start = getNextAlphabet(new_gram)

    new_gram.set_start(new_gram.start)
    new_gram.add_variable(new_gram.start)
    new_gram.add_rule([new_gram.start, gram.start])

    # Copiar todas as regras
    for rule in gram.rules_dict:
        for rul in gram.rules_dict[rule]:
            new_gram.add_rule([rule, rul])



    # 2 Remover λ-produções
    if debug:
        print("2. Removendo λ-produções\n")

    removeds = [] # Lista de regras removidas
    # Enquanto tiver regras lambda
    while new_gram.have_lambda(): 
    
        for rule in new_gram.rules_dict: # Para cada Variavel
            for rul in new_gram.rules_dict[rule]: # Para cada regra da variavel

                # Se a regra for lambda
                if rul == "λ":
                    if debug:
                        print("Removendo regra: {} -> {}".format(rule, rul))

                    try:
                        # Se a variavel não for a variavel inicial
                        if rule != new_gram.start:
                            new_gram.rules_dict[rule].remove(rul)
                            removeds.append([rule, rul])
                    except:
                        pass

                    # Adicionar regras
                    for rule2 in new_gram.rules_dict:
                        for rul2 in new_gram.rules_dict[rule2]:

                            # Ocorrencias de rule em rul2
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

                                combinations = list(substituicoes(rul2, rule, "λ"))
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
    
    # 3. Remover produções unitárias
    if debug:
        print("3. Removendo produções unitárias de variáveis\n")

    # Remover variavel que deriva ela mesma
    for rule in new_gram.rules_dict:
        for rul in new_gram.rules_dict[rule]:
            if rule == rul:
                new_gram.rules_dict[rule].remove(rul)
                pass


    # Enquanto tiver produções unitárias
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
                    # Adicionar todas as regras do rul para o rule
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

    # 4. Converte regras remanescentes
    if debug:
        print("4. Converte regras remanescentes\n")
    loop = 0

    # Enquanto não estiver na forma normal de Chomsky
    # Execute a remoção de regras remanescentes até que a gramática esteja na forma normal de Chomsky
    # Se entrar em loop, para
    while not new_gram.is_chomsky():
        loop += 1

        if loop > 100:
            print("Erro ao converter para Chomsky")
            break

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
                            # Alterar regra, removendo a regra antiga e adicionando a nova
                            new_gram.rules_dict[rule].remove(rul)
                            rulTmp = rul.replace(terminalTmp, gerador)

                            new_gram.add_rule([rule, rulTmp])

        # Tratar as regras que geram duas terminais
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

        # Tratar regras de 2 variáveis ou mais (remover regras de 3 variáveis ou mais)
        for rule in list(new_gram.rules_dict):
            for rul in new_gram.rules_dict[rule]:
                if len(rul) > 2:
                    # if all symbols are variables
                    for symbol in rul:
                        if not new_gram.is_variable(symbol):
                            break
                    if debug:
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
                        # Alterar regra, removendo a regra antiga e adicionando a nova
                        new_gram.rules_dict[rule].remove(rul)
                        rulTmp = rul.replace(twoFirst, gerador)

                        new_gram.add_rule([rule, rulTmp])          


    if debug:
        print("="*50)
        print("")



    return new_gram

def convertTo2NF(gram):
    """
    Converte gramática para 2NF
    """

    if gram.is_2nf():
        # Se já está em 2NF, não precisa converter
        return gram

    new_gram = gram.copy()
    loop = 0

    # Enquanto não estiver em 2NF
    # Se encontrar um loop, então pare
    while not new_gram.is_2nf():
        loop += 1
        if loop > 100:
            print("Erro ao converter para 2NF")
            break


        for rule in list(new_gram.rules_dict):      # Para cada regra
            for rul in new_gram.rules_dict[rule]:   # Para cada produção da regra

                # Se a produção tiver mais de 2 símbolos
                if len(rul) > 2: 

                    twoFirst = rul[:2] # Pegar os dois primeiros símbolos
                    gerador = False    # Variável geradora

                    for rule2 in new_gram.rules_dict:                   # Para cada regra
                        
                        rulesInRule2 = len(new_gram.rules_dict[rule2])  # Quantas produções tem na regra
                        if rulesInRule2 == 1:
                            # Se a regra tiver apenas uma produção
                            if new_gram.rules_dict[rule2][0] == twoFirst:
                                # Se a produção for igual aos dois primeiros símbolos
                                gerador = rule2
                                break
                    
                    
                    if not gerador:
                        # Se não encontrou uma variável geradora
                        gerador = getNextAlphabet(new_gram) # Pegar a próxima letra do alfabeto
    
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
