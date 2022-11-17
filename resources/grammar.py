# Digraph
#   - A directed graph
from graphviz import Digraph

# Classe que representa uma gramática.
class Grammar:
    def __init__(self):
        self.variables = []
        self.terminals = []
        self.start = ''
        self.rules_dict = {}

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

    def reachableFrom(self, state):
        reachable = set()
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                if state in rul:
                    reachable.add(rule)
        return reachable

    def reachableFromWithSymbol(self, state, symbol):
        reachable = set()
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                
                if state in rul or rul.startswith(symbol):
                    
                    reachable.add(rule)
        return reachable

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


    def graph(self, symbol):
        dot = Digraph()
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                # if symbol is str
                if symbol == str(symbol):
                    if symbol in rul:
                        dot.edge(rule, rul)
        return dot
       


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