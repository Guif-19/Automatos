#*Classe para Autômatos Não Deterministicos*

#Abreviações dos Atributos:
#Self = Passa os atributos aos métodos internos da classe
#Est = Conjunto de Estados
#Alf = Alfabeto
#Trs = Tabela de Transições (Feito em Dicionário, sendo a chave [Estado,Símbolo] e a saída os conjunto de próximos estados possíveis)
#Ini = Estado Inicial
#Fim = Estado Final

#Construtor do Objeto
class AFN:
    def __init__(Self, Est, Alf, Trs, Ini, Fim):
        Self.Est = Est
        Self.Alf = Alf
        Self.Trs = Trs
        Self.Ini = Ini
        Self.Fim = Fim

#*Verificação de Palvra AFN*

#A função começará no estado inicial, e para cada verificação de símbolo, é criado um conjunto com todos os próximos estados possíveis
#com base na tabela de transição, os quais seguirão o mesmo processo um por um, até o fim da palavra, com a lógica semelhante a de uma árvore
#cobrindo assim todas as possibilidades de caminhos.
#Por fim, retorna se algum dos estados resultantes é aceito como final.
    def Verif_palavra(Self, Entrada):
        Atuais = {Self.Ini}
        for Simbolo in Entrada:
            Proximos = set()
            for Estado in Atuais:
                if (Estado, Simbolo) in Self.Trs and Self.Trs[(Estado, Simbolo)] is not None:
                    Proximos.update(Self.Trs[(Estado, Simbolo)])
            Atuais = Proximos
        return not Atuais.isdisjoint(Self.Fim)

#Função padrão de exibição do autômato
    def __str__(Self):
        Atr = ("\n-AFN Armazenado-\n\n"
                f"Estados: {Self.Est}\n"
                f"Alfabeto: {Self.Alf}\n"
                f"Transições: {Self.Trs}\n"
                f"Estado Inicial: {Self.Ini}\n"
                f"Estados Finais: {Self.Fim}\n")
        return Atr


#*Classe para Autômatos Deterministicos*

#Atributos semelhantes ao AFN, porém, seguindo a lógica do AFD,
#não é permitido transições diferentes em um estado usando um mesmo símbolo.
#Porém, esse problema será tratado na digitação da entrada no arquivo principal.

#Construtor do Objeto
class AFD:
    def __init__(Self, Est, Alf, Trs, Ini, Fim):
        Self.Est = Est
        Self.Alf = Alf
        Self.Trs = Trs
        Self.Ini = Ini
        Self.Fim = Fim

#*Verificação de Palvra AFN*

#A função começará no estado inicial, e então com base na tabela de transições, percorre o caminho
#de estados para cada símbolo da palavra.
#Ao fim, retorna se o estado atual é aceito como final.
    def Verif_Palavra(Self, Entrada):
        Atual = Self.Ini
        for Simbolo in Entrada: 
            if Simbolo not in Self.Alf:
                return "erroalf"
            if (Atual, Simbolo) in Self.Trs:
                Atual = Self.Trs[(Atual, Simbolo)]
            if Atual is None:
                return False
        return Atual in Self.Fim
    
#Função padrão de exibição do autômato
    def __str__(Self):
        Atr = ("\n-AFD Armazenado-\n\n"
                f"Estados: {Self.Est}\n"
                f"Alfabeto: {Self.Alf}\n"
                f"Transições: {Self.Trs}\n"
                f"Estado Inicial: {Self.Ini}\n"
                f"Estados Finais: {Self.Fim}\n")
        return Atr