class NFA:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        """
        Inicializa um autômato finito não-determinístico (NFA).

        estados: Conjunto de estados do NFA.
        alfabeto: Conjunto de símbolos do alfabeto do NFA.
        transicoes: Dicionário de transições onde a chave é uma tupla (estado, símbolo)
        e o valor é um conjunto de estados.

        estado_inicial: Estado inicial do NFA.
        estados_aceitacao: Conjunto de estados de aceitação do NFA.
        """
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def aceita(self, palavra):
        """
        Verifica se o NFA aceita uma palavra.

        palavra: Palavra a ser verificada.
        return True se a palavra é aceita, False caso contrário.
        """
        estados_atuais = {self.estado_inicial}
        for simbolo in palavra:
            proximos_estados = set()
            for estado in estados_atuais:
                if (estado, simbolo) in self.transicoes:
                    proximos_estados.update(self.transicoes[(estado, simbolo)])
            estados_atuais = proximos_estados
        return not estados_atuais.isdisjoint(self.estados_aceitacao)


class DFA:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        """
        Inicializa um autômato finito determinístico (DFA).

        estados: Conjunto de estados do DFA.
        alfabeto: Conjunto de símbolos do alfabeto do DFA.
        transicoes: Dicionário de transições onde a chave é uma tupla (estado, símbolo) e o valor é um estado.
        estado_inicial: Estado inicial do DFA.
        estados_aceitacao: Conjunto de estados de aceitação do DFA.
        """
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def aceita(self, palavra):
        """
        Verifica se o DFA aceita uma palavra.

        palavra: Palavra a ser verificada.
        return: True se a palavra é aceita, False caso contrário.
        """
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            if (estado_atual, simbolo) in self.transicoes:
                estado_atual = self.transicoes[(estado_atual, simbolo)]
            else:
                return False
        return estado_atual in self.estados_aceitacao


def converter_nfa_para_dfa(nfa):
    """
    Converte um NFA em um DFA equivalente.

    nfa: Instância do NFA a ser convertido.
    return: Instância do DFA equivalente.
    """
    estados_dfa = {frozenset([nfa.estado_inicial])}
    estado_inicial_dfa = frozenset([nfa.estado_inicial])
    estados_aceitacao_dfa = set()
    transicoes_dfa = {}
    estados_nao_marcados = [frozenset([nfa.estado_inicial])]

    while estados_nao_marcados:
        atual = estados_nao_marcados.pop()
        if not atual.isdisjoint(nfa.estados_aceitacao):
            estados_aceitacao_dfa.add(atual)
        for simbolo in nfa.alfabeto:
            proximo_estado = set()
            for estado in atual:
                if (estado, simbolo) in nfa.transicoes:
                    proximo_estado.update(nfa.transicoes[(estado, simbolo)])
            proximo_estado = frozenset(proximo_estado)
            if proximo_estado:
                if proximo_estado not in estados_dfa:
                    estados_dfa.add(proximo_estado)
                    estados_nao_marcados.append(proximo_estado)
                transicoes_dfa[(atual, simbolo)] = proximo_estado

    return DFA(estados_dfa, nfa.alfabeto, transicoes_dfa, estado_inicial_dfa, estados_aceitacao_dfa)


def minimizar_dfa(dfa):
    """
    Minimiza um DFA removendo estados redundantes.

    dfa: Instância do DFA a ser minimizado.
    return: Instância do DFA minimizado.
    """
    particoes = [dfa.estados_aceitacao, dfa.estados - dfa.estados_aceitacao]
    while True:
        novas_particoes = []
        for particao in particoes:
            divisao = {}
            for estado in particao:
                chave = tuple(frozenset(
                    {(estado, simbolo): dfa.transicoes.get((estado, simbolo), None) for simbolo in dfa.alfabeto}))
                if chave not in divisao:
                    divisao[chave] = set()
                divisao[chave].add(estado)
            novas_particoes.extend(divisao.values())
        if len(novas_particoes) == len(particoes):
            break
        particoes = novas_particoes

    mapeamento_estados = {estado: i for i, particao in enumerate(particoes) for estado in particao}
    novos_estados = set(mapeamento_estados.values())
    novo_estado_inicial = mapeamento_estados[dfa.estado_inicial]
    novos_estados_aceitacao = {mapeamento_estados[estado] for estado in dfa.estados_aceitacao}
    novas_transicoes = {}
    for (estado, simbolo), proximo_estado in dfa.transicoes.items():
        novas_transicoes[(mapeamento_estados[estado], simbolo)] = mapeamento_estados[proximo_estado]

    return DFA(novos_estados, dfa.alfabeto, novas_transicoes, novo_estado_inicial, novos_estados_aceitacao)


def demonstrar_equivalencia(nfa, dfa, palavras_teste):
    """
    Verifica a equivalência entre um NFA e um DFA usando palavras de teste.

    nfa: Instância do NFA.
    dfa: Instância do DFA.
    palavras_teste: Lista de palavras para testar equivalência.
    return: True se o NFA e o DFA são equivalentes, False caso contrário.
    """
    for palavra in palavras_teste:
        if nfa.aceita(palavra) != dfa.aceita(palavra):
            return False
    return True


def main():
    """
    Função principal que lê a entrada do usuário e executa as operações principais.
    """
    estados = set(input("Estados (separados por espaço): ").split())
    alfabeto = set(input("Alfabeto (separados por espaço): ").split())
    transicoes = {}
    print("Transições (no formato 'estado símbolo estado_destino'):")
    while True:
        transicao = input()
        if not transicao:
            break
        partes = transicao.split()
        if len(partes) != 3:
            print("Entrada inválida. Tente novamente.")
            continue
        estado, simbolo, estado_destino = partes
        if (estado, simbolo) not in transicoes:
            transicoes[(estado, simbolo)] = set()
        transicoes[(estado, simbolo)].add(estado_destino)

    estado_inicial = input("Estado inicial: ")
    estados_aceitacao = set(input("Estados de aceitação (separados por espaço): ").split())

    nfa = NFA(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
    dfa = converter_nfa_para_dfa(nfa)
    dfa_minimizado = minimizar_dfa(dfa)

    while True:
        palavra = input("Digite uma palavra para verificar (ou 'sair' para encerrar): ")
        if palavra == 'sair':
            break
        print(f"AFN aceita a palavra? {'Sim' if nfa.aceita(palavra) else 'Não'}")
        print(f"AFD aceita a palavra? {'Sim' if dfa.aceita(palavra) else 'Não'}")
        print(f"AFD Minimizado aceita a palavra? {'Sim' if dfa_minimizado.aceita(palavra) else 'Não'}")

    palavras_teste = input("Palavras de teste (separadas por espaço): ").split()
    equivalencia = demonstrar_equivalencia(nfa, dfa, palavras_teste)
    print(f"AFN e AFD são equivalentes? {'Sim' if equivalencia else 'Não'}")


if __name__ == "__main__":
    main()
