#Definição das classes para AFN e AFD

class Automaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

class DFA(Automaton):
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        super().__init__(states, alphabet, transitions, start_state, accept_states)

    def accepts(self, word):
        current_state = self.start_state
        for symbol in word:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
            else:
                return False
        return current_state in self.accept_states

class NFA(Automaton):
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        super().__init__(states, alphabet, transitions, start_state, accept_states)

    def accepts(self, word):
        current_states = {self.start_state}
        for symbol in word:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            current_states = next_states
        return bool(current_states.intersection(self.accept_states))

#Conversão de AFN para AFD


def convert_nfa_to_dfa(nfa):
    dfa_states = {}
    dfa_transitions = {}
    dfa_start_state = frozenset([nfa.start_state])
    dfa_accept_states = set()

    queue = [dfa_start_state]
    dfa_states[dfa_start_state] = True

    while queue:
        current_dfa_state = queue.pop(0)
        for symbol in nfa.alphabet:
            next_dfa_state = set()
            for state in current_dfa_state:
                if (state, symbol) in nfa.transitions:
                    next_dfa_state.update(nfa.transitions[(state, symbol)])
            next_dfa_state = frozenset(next_dfa_state)
            if next_dfa_state:
                dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state
                if next_dfa_state not in dfa_states:
                    dfa_states[next_dfa_state] = True
                    queue.append(next_dfa_state)

    for dfa_state in dfa_states:
        if dfa_state.intersection(nfa.accept_states):
            dfa_accept_states.add(dfa_state)

    return DFA(
        states=set(dfa_states.keys()),
        alphabet=nfa.alphabet,
        transitions=dfa_transitions,
        start_state=dfa_start_state,
        accept_states=dfa_accept_states
    )


#Simulação de Aceitação de Palavras Já foi implementada
#a simulação de aceitação de palavras nas classes DFA e NFA.

#Demonstração de Equivalência

def demonstrate_equivalence(nfa, dfa, test_words):
    for word in test_words:
        if nfa.accepts(word) != dfa.accepts(word):
            return False
    return True


#Minimização de AFDs


def minimize_dfa(dfa):
    P = [dfa.accept_states, dfa.states - dfa.accept_states]
    W = [dfa.accept_states, dfa.states - dfa.accept_states]

    while W:
        A = W.pop()
        for c in dfa.alphabet:
            X = {state for state in dfa.states if (state, c) in dfa.transitions and dfa.transitions[(state, c)] in A}
            for Y in P:
                intersection = X.intersection(Y)
                difference = Y.difference(X)
                if intersection and difference:
                    P.remove(Y)
                    P.append(intersection)
                    P.append(difference)
                    if Y in W:
                        W.remove(Y)
                        W.append(intersection)
                        W.append(difference)
                    else:
                        if len(intersection) <= len(difference):
                            W.append(intersection)
                        else:
                            W.append(difference)

    new_states = set(frozenset(partition) for partition in P)
    new_start_state = next(state for state in new_states if dfa.start_state in state)
    new_accept_states = set(state for state in new_states if state.intersection(dfa.accept_states))
    new_transitions = {}

    for state in new_states:
        for c in dfa.alphabet:
            if any((substate, c) in dfa.transitions for substate in state):
                next_state = next(
                    frozenset(partition) for partition in P
                    if dfa.transitions[(next(iter(state)), c)] in partition
                )
                new_transitions[(state, c)] = next_state

    return DFA(
        states=new_states,
        alphabet=dfa.alphabet,
        transitions=new_transitions,
        start_state=new_start_state,
        accept_states=new_accept_states
    )


#Construção de um Front-end Simples

def main():
    states = set(input("Estados (separados por espaço): ").split())
    alphabet = set(input("Alfabeto (separados por espaço): ").split())
    transitions = {}
    print("Transições (no formato 'estado símbolo estado_destino'):")
    while True:
        transition = input()
        if not transition:
            break
        state, symbol, next_state = transition.split()
        if (state, symbol) not in transitions:
            transitions[(state, symbol)] = set()
        transitions[(state, symbol)].add(next_state)
    start_state = input("Estado inicial: ")
    accept_states = set(input("Estados de aceitação (separados por espaço): ").split())

    nfa = NFA(states, alphabet, transitions, start_state, accept_states)
    dfa = convert_nfa_to_dfa(nfa)
    minimized_dfa = minimize_dfa(dfa)

    while True:
        word = input("Digite uma palavra para verificar (ou 'sair' para encerrar): ")
        if word == 'sair':
            break
        print(f"AFN aceita a palavra? {'Sim' if nfa.accepts(word) else 'Não'}")
        print(f"AFD aceita a palavra? {'Sim' if dfa.accepts(word) else 'Não'}")
        print(f"AFD Minimizado aceita a palavra? {'Sim' if minimized_dfa.accepts(word) else 'Não'}")

    test_words = input("Palavras de teste (separadas por espaço): ").split()
    equivalence = demonstrate_equivalence(nfa, dfa, test_words)
    print(f"AFN e AFD são equivalentes? {'Sim' if equivalence else 'Não'}")


if __name__ == "__main__":
    main()
