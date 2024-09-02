################################################
# Classe do Autômato Finito Não Deterministico #
################################################
class AFN:
    def __init__(self, estados, alfabeto, transicao, inicial, finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicao = transicao
        self.inicial = inicial
        self.finais = finais

#Verificação de palavra AFN
    def verificar_palavra(self, entrada):
        atuais = {self.inicial}
        for simbolo in entrada:
            proximos = set()
            for estado in atuais:
                if (estado, simbolo) in self.transicao and self.transicao[(estado, simbolo)] is not None:
                    proximos.update(self.transicao[(estado, simbolo)])
            atuais = proximos
        return not atuais.isdisjoint(self.finais)

#Função padrão de exibição do autômato
    def __str__(self):
        atr = ("\n-AFN Armazenado-\n\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Transições: {self.transicao}\n"
                f"Estado Inicial: {self.inicial}\n"
                f"Estados Finais: {self.finais}\n")
        return atr



############################################
# Classe do Autômato Finito Deterministico #
############################################
class AFD:
    def __init__(self, estados, alfabeto, transicao, inicial, finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicao = transicao
        self.inicial = inicial
        self.finais = finais

#Verificação de palavra do AFD
    def verificar_palavra(self, entrada):
        atual = self.inicial
        for simbolo in entrada: 
            if simbolo not in self.alfabeto:
                return False
            if (atual, simbolo) in self.transicao:
                atual = self.transicao[(atual, simbolo)]
            if atual is None:
                return False
        return atual in self.finais

#Função padrão de exibição do autômato    
    def __str__(self):
        atr = ("\n-AFD Armazenado-\n\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Transições: {self.transicao}\n"
                f"Estado Inicial: {self.inicial}\n"
                f"Estados Finais: {self.finais}\n")
        return atr