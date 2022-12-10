# Fundamentos Teóricos da Computação
# Trabalho Prático 2
# Implementação do algoritmo CYK e CYK-M
# Gustavo Torres Bretas Alves - 689655
# Maria Fernanda Oliveira Guimarães - 690667

class Grammar:
    """
    Classe que representa uma gramática.
    :param variables: Lista de variáveis.
    :param terminals: Lista de terminais.
    :param start: Variável inicial.
    :param rules_dict: Dicionário de regras.
    """
    def __init__(self):
        self.variables = []
        self.terminals = []
        self.start = ''
        self.rules_dict = {}

    def add_variable(self, variable):
        """
        Adiciona uma variável à gramática.
        :param variable: Variável a ser adicionada.
        """
        
        self.variables.append(variable)

    def add_terminal(self, terminal):
        """
        Adiciona um terminal à gramática.
        :param terminal: Terminal a ser adicionado.
        """
        self.terminals.append(terminal)

    def set_start(self, start):
        """
        Define a variável inicial da gramática.
        :param start: Variável inicial.
        """
        self.start = start

    def get_start(self):
        """
        Retorna a variável inicial da gramática.
        """
        return self.start
    
    def get_rules(self, variable):
        """
        Retorna as regras de uma variável.
        :param variable: Variável.
        """
        return self.rules_dict[variable]

    def is_terminal(self, symbol):
        """
        Checa se um símbolo é terminal.
        :param symbol: Símbolo a ser checado.
        """
        return symbol in self.terminals

    def is_variable(self, symbol):
        """
        Checa se um símbolo é variável.
        :param symbol: Símbolo a ser checado.
        """
        return symbol in self.variables

   
    def is_context_free(self):
        """
        Checa se a gramática é livre de contexto.
        """

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

    def is_chomsky(self):
        """
        Checa se a gramática é na forma normal de Chomsky.
        """
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
               
    

    def is_2nf(self):
        """
        Checa se a gramática é na forma normal de Chomsky.
        """
        for rule in self.rules_dict: # Para cada Variavel
            for rul in self.rules_dict[rule]: # Para cada regra da variavel
                if len(rul) > 2:
                    return False

        return True

    def have_lambda(self):
        """
        Checa se a gramática possui regras lambda em váriaveis que não são a inicial.
        """
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                if rul == "λ" and rule != self.start:
                    return True
        return False

    def have_unitary(self):
        """
        Checa se a gramática possui regras unitárias.
        """
        for rule in self.rules_dict:
            for rul in self.rules_dict[rule]:
                if len(rul) == 1 and rul != "λ" and self.is_variable(rul):
                    return True
        return False

    def add_rule(self, rule):
        """
        Adiciona uma regra à gramática.
        :param rule: Regra a ser adicionada.
        """
        if rule[0] not in self.rules_dict:
            self.rules_dict[rule[0]] = []
            for rul in rule[1::]:
                self.rules_dict[rule[0]].append(rul)
        else:
            for rul in rule[1::]:
                if rul not in self.rules_dict[rule[0]]:
                    self.rules_dict[rule[0]].append(rul)

    def copy(self):
        """
        Retorna uma cópia da gramática.
        """
        grammar = Grammar()
        grammar.variables = self.variables.copy()
        grammar.terminals = self.terminals.copy()
        grammar.start = self.start
        grammar.rules_dict = self.rules_dict.copy()
        return grammar
        

    def __str__(self):
        """
        Retorna uma string da gramática.
        """
        regras_formatadas = "\n"
        for rule in self.rules_dict:
            regras_formatadas += "  "+rule + " -> "
            for rul in self.rules_dict[rule]:
                regras_formatadas += rul + " | "
            regras_formatadas = regras_formatadas[:-3]
            regras_formatadas += "\n"
            

        return 'Variáveis: {}\nTerminais: {}\nInício: {}\nRegras: {}'.format(self.variables, self.terminals, self.start, regras_formatadas)

    def __repr__(self):
        """
        Retorna uma string da gramática.
        """
        return self.__str__()