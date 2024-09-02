##################
# Menu Principal #
##################
import Automatos
import Funcoes 
import Turing

def main():
    print("\nSimulador de Autômatos\n\n"
        "Rafael Souza Tavares de Castro-8179\n"
        "Guilherme Francisco de Sousa Costa-7555\n\n")
    
#Escolha do tipo de autômato da entrada    
    tipo = input("Selecione qual autômato deseja inserir (AFD, AFN ou TURING): ").upper()

#Preenchimento no caso de uma Máquina de Turing
    if(tipo == "TURING"):
        estados = set(input("Estados (Separados por espaço): ").split())
        alfabeto_entrada = set(input("Alfabeto de Entrada (Separados por espaço): ").split())
        alfabeto_fita = set(input("Alfabeto da Fita (Separados por espaço): ").split())
        marca_inicio = input("Símbolo de Marcação do Início: ")
        vazio = input("Símbolo de Espaços Vazios: ")
        transicoes = {}

        print("\nTransições (no formato 'Estado Atual' 'Simbolo' 'Novo Estado' 'Simbolo Escrito' 'Direção')\n"
            "Para terminar, aperte 2 vezes Enter:"
            "Exemplo: 0 a 0 b >")
        while True:
            transicao = input()
            if not transicao:
                break
            elemento = transicao.split()
            if len(elemento) != 5:
                print("Entrada inválida. Tente novamente.")
                continue
            estado, simbolo, destino, escrito, direcao = elemento
            t = (estado, simbolo)
            tuple(t)
            if t not in transicoes:
                transicoes[t] = destino, escrito, direcao
            else:
                print("Transição já existente para esse símbolo nesse estado. Tente novamente.")

        inicial = input("Estado inicial: ")
        finais = set(input("Estados de aceitação (separados por espaço): ").split())

        t = Turing.MaquinaTuring(estados, alfabeto_entrada, alfabeto_fita, marca_inicio, vazio, transicoes, inicial, finais, fita=['default'])
        Funcoes.imprimir_turing(t)

        while True:
            palavra = input("\nDigite uma palavra para computar (ou 'sair' para encerrar): ")
            t = Turing.MaquinaTuring(estados, alfabeto_entrada, alfabeto_fita, marca_inicio, vazio, transicoes, inicial, finais, fita=palavra)
            if palavra == 'sair':
                break
            else:
                t.executar()
                print(f"\nO resultado da Maquina de Turing: {t.obter_fita()}")        
        
#Preenchimento dos parâmetros do autômato
    else:
        estados = set(input("Estados (Separados por espaço): ").split())
        alfabeto = set(input("Alfabeto (Separados por espaço): ").split())
        transicoes = {}

        print("\nTransições (no formato 'Estado' 'Simbolo' 'Próximo Estado')\n"
            "Para terminar, aperte 2 vezes Enter:")
        while True:
            transicao = input()
            if not transicao:
                break
            elemento = transicao.split()
            if len(elemento) != 3:
                print("Entrada inválida. Tente novamente.")
                continue
            estado, simbolo, destino = elemento
            t = (estado, simbolo)
            tuple(t)
            if(tipo == 'AFD'):
                if t not in transicoes:
                    transicoes[t] = None
                    transicoes[t] = destino
                else:
                    print("Transição já existente para esse símbolo nesse estado. Tente novamente.")
            if(tipo == 'AFN'):
                if t not in transicoes:
                    transicoes[t] = set()
                transicoes[t].add(destino)             

        estado_inicial = input("Estado inicial: ")
        estados_finais = set(input("Estados de aceitação (separados por espaço): ").split())

        if(tipo == 'AFD'):
            afd = Automatos.AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            print(afd)
        if(tipo == 'AFN'):
            afn = Automatos.AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)
            convertido_afd = Funcoes.conversor_afn_para_afd(afn)
            Funcoes.imprimir_afn(afn)
            print("\nAFN convertido em AFD")
            Funcoes.imprimir_afd(convertido_afd)

    #Faz o teste de aceitação com a palavra digitada
        while True:
            palavra = input("\nDigite uma palavra para verificar (ou 'sair' para encerrar): ")
            if palavra == 'sair':
                break
            if(tipo == 'AFD'):
                print(f"\nO AFD aceita a palavra? {'Sim' if afd.verificar_palavra(palavra) else 'Não'}")
            if(tipo == 'AFN'):
                print(f"\nO AFN aceita a palavra? {'Sim' if afn.verificar_palavra(palavra) else 'Não'}")
                print(f"\nO AFD convertido aceita a palavra? {'Sim' if convertido_afd.verificar_palavra(palavra) else 'Não'}")

if __name__ == "__main__":
    main()
