import tkinter as tk
from tkinter import messagebox
from graphviz import Digraph

class NFA:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def aceita(self, palavra):
        estados_atuais = {self.estado_inicial}
        for simbolo in palavra:
            novos_estados = set()
            for estado in estados_atuais:
                if (estado, simbolo) in self.transicoes:
                    novos_estados.update(self.transicoes[(estado, simbolo)])
            estados_atuais = novos_estados
        return any(estado in self.estados_aceitacao for estado in estados_atuais)


class DFA:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def aceita(self, palavra):
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            if (estado_atual, simbolo) in self.transicoes:
                estado_atual = self.transicoes[(estado_atual, simbolo)]
            else:
                return False
        return estado_atual in self.estados_aceitacao


def converter_nfa_para_dfa(nfa):
    novo_estado_inicial = frozenset([nfa.estado_inicial])
    novos_estados = {novo_estado_inicial}
    novas_transicoes = {}
    estados_aceitacao = set()
    estados_a_processar = [novo_estado_inicial]
    processados = set()

    while estados_a_processar:
        estado_atual = estados_a_processar.pop()
        processados.add(estado_atual)

        for simbolo in nfa.alfabeto:
            novos_estados_destino = set()
            for subestado in estado_atual:
                if (subestado, simbolo) in nfa.transicoes:
                    novos_estados_destino.update(nfa.transicoes[(subestado, simbolo)])

            novo_estado = frozenset(novos_estados_destino)
            novas_transicoes[(estado_atual, simbolo)] = novo_estado

            if novo_estado not in novos_estados:
                novos_estados.add(novo_estado)

            if novo_estado not in processados:
                estados_a_processar.append(novo_estado)

        if any(subestado in nfa.estados_aceitacao for subestado in estado_atual):
            estados_aceitacao.add(estado_atual)

    return DFA(novos_estados, nfa.alfabeto, novas_transicoes, novo_estado_inicial, estados_aceitacao)


def imprimir_nfa(nfa):
    print("\nNFA:")
    print("Estados:", nfa.estados)
    print("Alfabeto:", nfa.alfabeto)
    print("Transições:")
    for (estado, simbolo), estados_destino in nfa.transicoes.items():
        for estado_destino in estados_destino:
            print(f" {estado} --{simbolo}--> {estado_destino}")
    print("Estado inicial:", nfa.estado_inicial)
    print("Estados de aceitação:", nfa.estados_aceitacao)


def imprimir_dfa(dfa):
    print("\nDFA:")
    print("Estados:", dfa.estados)
    print("Alfabeto:", dfa.alfabeto)
    print("Transições:")
    for (estado, simbolo), estado_destino in dfa.transicoes.items():
        print(f" {estado} --{simbolo}--> {estado_destino}")
    print("Estado inicial:", dfa.estado_inicial)
    print("Estados de aceitação:", dfa.estados_aceitacao)


def testar_palavra(automato, palavra, tipo_automato):
    aceita = automato.aceita(palavra)
    print(f"A palavra '{palavra}' {'é aceita' if aceita else 'NÃO é aceita'} pelo {tipo_automato}.")


def main():
    tipo = input("Tipo de automato (NFA ou DFA): ").strip().upper()
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
        if tipo == "NFA":
            if (estado, simbolo) not in transicoes:
                transicoes[(estado, simbolo)] = set()
            transicoes[(estado, simbolo)].add(estado_destino)
        elif tipo == "DFA":
            transicoes[(estado, simbolo)] = estado_destino

    estado_inicial = input("Estado inicial: ")
    estados_aceitacao = set(input("Estados de aceitação (separados por espaço): ").split())

    if tipo == "NFA":
        nfa = NFA(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
        imprimir_nfa(nfa)
        dfa = converter_nfa_para_dfa(nfa)
        imprimir_dfa(dfa)
    else:
        dfa = DFA(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
        imprimir_dfa(dfa)

    while True:
        palavra = input("Digite uma palavra para verificar (ou 'sair' para encerrar): ")
        if palavra == 'sair':
            break

        if tipo == "NFA":
            testar_palavra(nfa, palavra, "NFA")
            testar_palavra(dfa, palavra, "DFA")
        else:
            testar_palavra(dfa, palavra, "DFA")


if __name__ == "__main__":
    main()