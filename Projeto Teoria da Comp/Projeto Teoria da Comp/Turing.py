#####################
# Maquina de Turing #
#####################
class MaquinaTuring:
    def __init__(self, estados, alfabeto_entrada, alfabeto_fita, marca_inicio, vazio, transicao, inicial, finais, fita):
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_fita = alfabeto_fita
        self.marca_inicio = marca_inicio
        self.vazio = vazio
        self.transicao = transicao
        self.inicial = inicial
        self.finais = finais
        self.fita = [self.marca_inicio] + list(fita) + [self.vazio]
        self.cabeca = 1
        self.atual = self.inicial
    
    def executar(self, max_passos=999):
        passos = 0
        while self.atual not in self.finais and passos < max_passos:
            leitura = self.fita[self.cabeca]
            if (self.atual, leitura) in self.transicao:
                novo_estado, escrever, mover = self.transicao[(self.atual, leitura)]
                self.fita[self.cabeca] = escrever
                self.atual = novo_estado
                if mover == '>':
                    self.cabeca += 1
                elif mover == '<':
                    self.cabeca -= 1
            else:
                break
            passos += 1
    
    def obter_fita(self):
        return ''.join(self.fita).strip(self.marca_inicio).strip(self.vazio)
    
    def mudar_fita(self, fita_input):
        self.fita = [self.marca_inicio] + list(fita_input) + [self.vazio]