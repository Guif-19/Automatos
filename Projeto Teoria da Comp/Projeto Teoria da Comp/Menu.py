import Automatos 

def main():

    print("\nSimulador de Automatos\n\n"
        "Rafael Souza Tavares de Castro-8179\n"
        "Guilherme Francisco de Sousa Costa- 7555\n\n")
    
    x = input("Selecione qual automato deseja inserir (1-AFD ou 2-AFN): ")

    Estados = set(input("Estados (separados por espaço): ").split())
    Alfabeto = set(input("Alfabeto (separados por espaço): ").split())
    Transicoes = {}

    print("\nTransições (no formato 'Estado' 'Simbolo' 'Proximo Estado')\n"
          "Para terminar, aperte 2 vezes Enter:")
    while True:
        Trans = input()
        if not Trans:
            break
        Elem = Trans.split()
        if len(Elem) != 3:
            print("Entrada inválida. Tente novamente.")
            continue
        Estado, Simbolo, Destino = Elem
        T = (Estado, Simbolo)
        tuple(T)
        if(x == '1'):
            if T not in Transicoes:
                Transicoes[T] = None
                Transicoes[T] = Destino
            else:
                print("Transição já existente para esse símbolo nesse estado. Tente novamente.")
        if(x == '2'):
            if T not in Transicoes:
                Transicoes[T] = set()
            Transicoes[T].add(Destino)             

    Estado_Inicial = input("Estado inicial: ")
    Estados_Finais = set(input("Estados de aceitação (separados por espaço): ").split())

    if(x == '1'):
        Afd = Automatos.AFD(Estados, Alfabeto, Transicoes, Estado_Inicial, Estados_Finais)
        print(Afd)
    if(x == '2'):
        Afn = Automatos.AFN(Estados, Alfabeto, Transicoes, Estado_Inicial, Estados_Finais)
        print(Afn)

    while True:
        Palavra = input("\nDigite uma palavra para verificar (ou 'sair' para encerrar): ")
        if Palavra == 'sair':
            break
        if(x == '1'):
            print(f"\nO AFD aceita a palavra? {'Sim' if Afd.Verif_Palavra(Palavra) else 'Não'}")
        if(x == '2'):
            print(f"\nO AFN aceita a palavra? {'Sim' if Afn.Verif_palavra(Palavra) else 'Não'}")

if __name__ == "__main__":
    main()
