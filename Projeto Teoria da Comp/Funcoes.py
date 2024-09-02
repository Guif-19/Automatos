#############################
# Funções para os autômatos #
#############################
import Automatos 

#Conversor de AFN para AFD
def conversor_afn_para_afd(afn):
    x=0
    novo_inicial = frozenset([afn.inicial])
    novos_estados = {novo_inicial}
    novas_transicoes = {}
    novos_finais = set()
    estados_a_processar = [novo_inicial]
    processados = set()

    while estados_a_processar:
        atual = estados_a_processar.pop()
        processados.add(atual)

        for simbolo in afn.alfabeto:
            novos_destino = set()
            for sub_estado in atual:
                if (sub_estado, simbolo) in afn.transicao:
                    novos_destino.update(afn.transicao[(sub_estado, simbolo)])

            novo_estado = frozenset(novos_destino)
            novas_transicoes[(atual, simbolo)] = novo_estado

            if novo_estado not in novos_estados:
                novos_estados.add(novo_estado)

            if novo_estado not in processados:
                estados_a_processar.append(novo_estado)

        if any(sub_estado in afn.finais for sub_estado in atual):
            novos_finais.add(atual)

    return Automatos.AFD(novos_estados, afn.alfabeto, novas_transicoes, novo_inicial, novos_finais)



#Função de impressão do AFN
def imprimir_afn(afn):
    print("\nNFA:")
    print("Estados:", afn.estados)
    print("Alfabeto:", afn.alfabeto)
    print("Transições:")
    for (estado, simbolo), estados_destino in afn.transicao.items():
        for estado_destino in estados_destino:
            print(f" {estado} --{simbolo}--> {estado_destino}")
    print("Estado inicial:", afn.inicial)
    print("Estados de aceitação:", afn.finais)

#Função de impressão do AFD
def imprimir_afd(afd):
    print("\nDFA:")
    print("Estados:", afd.estados)
    print("Alfabeto:", afd.alfabeto)
    print("Transições:")
    for (estado, simbolo), estado_destino in afd.transicao.items():
        print(f" {estado} --{simbolo}--> {estado_destino}")
    print("Estado inicial:", afd.inicial)
    print("Estados de aceitação:", afd.finais)