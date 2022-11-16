from grammar import Grammar
import random
debug = False
# Função que pega a próxima letra do alfabeto.
def getNextAlphabet(gram):
    nextAlpha = chr(ord('A') + len(gram.variables))
    while nextAlpha in gram.variables:
        # get random alpha from A-Z
        nextAlpha = chr(ord('A') + random.randint(0, 25))

    return nextAlpha
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
    loop = 0
    while not new_gram.is_chomsky():
    # for loop in range(1):

        loop += 1

        if loop > 100:
            print("Erro ao converter para Chomsky")
            break
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

        # print(new_gram)
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
    loop = 0
    while not new_gram.is_2nf():
        loop += 1
        if loop > 100:
            print("Erro ao converter para 2NF")
            break
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
