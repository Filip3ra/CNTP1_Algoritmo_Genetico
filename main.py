import numpy as np
import random

# guarda a posição do melhor pai da geração atual
melhor_pai = [0, 0]


# função fitness, que transforma os valores binários em um valor inteiro
def sinal_saida(v):
    r = (9 + (int(v[2]) * int(v[5])) - (int(v[23]) * int(v[14]))
         + (int(v[24]) * int(v[4])) - (int(v[21]) * int(v[10]))
         + (int(v[36]) * int(v[15])) - (int(v[11]) * int(v[26]))
         + (int(v[16]) * int(v[17])) + (int(v[3]) * int(v[33]))
         + (int(v[28]) * int(v[19])) + (int(v[12]) * int(v[34]))
         - (int(v[31]) * int(v[32])) - (int(v[22]) * int(v[25]))
         + (int(v[35]) * int(v[27])) - (int(v[29]) * int(v[7]))
         + (int(v[8]) * int(v[13])) - (int(v[6]) * int(v[9]))
         + (int(v[18]) * int(v[20])) - (int(v[1]) * int(v[30]))
         + (int(v[23]) * int(v[4])) + (int(v[21]) * int(v[15]))
         + (int(v[26]) * int(v[16])) + (int(v[31]) * int(v[12]))
         + (int(v[25]) * int(v[19])) + (int(v[7]) * int(v[8]))
         + (int(v[9]) * int(v[18])) + (int(v[1]) * int(v[33])))
    return r


# Função que converte inteiro para binário, onde cada bit é um caractere char.
# Adiciono um zero inicial em 'vet_num' para facilitar o acesso na função fitness,
# que acessa da posição 1 até 36.
def int_pra_bin(vet_int):
    vet_char_bin = '0'
    for x in range(9):
        num_bin = "{0:{fill}4b}".format(vet_int[x], fill='0')  # converte o inteiro em binário, 4 bits
        vet_char_bin += num_bin  # salvo cada bit como um caractere
    return vet_char_bin


# Função que realiza o torneio binário, retornando um vetor com as posições
# na matriz de individuos referente aos vencedores do torneio.
def torneio_binario():
    # declaro uma lista vazia para guardar os vencedores do torneio
    ganhadores = []

    # realizo o torneio 30 vezes para manter 30 indivíduos
    for a in range(30):

        # escolho dois individuos de forma aleatória
        p1 = p2 = 0
        while p1 == p2:
            p1 = random.randint(0, 29)
            p2 = random.randint(0, 29)

        # faço um torneio binário entre p1 e p2
        fitness_p1 = sinal_saida(int_pra_bin(individuos[p1]))
        fitness_p2 = sinal_saida(int_pra_bin(individuos[p2]))

        # quem for maior passa no torneio
        if fitness_p1 > fitness_p2:
            #print("P1 passa = ", fitness_p1)
            ganhadores.append(p1)

            # verifico quem é o melhor pai
            if fitness_p1 > melhor_pai[1]:
                melhor_pai[0] = p1
                melhor_pai[1] = fitness_p1
        elif fitness_p1 < fitness_p2:
            #print("P2 passa = ", fitness_p2)
            ganhadores.append(p2)

            if fitness_p2 > melhor_pai[1]:
                melhor_pai[0] = p2
                melhor_pai[1] = fitness_p2
        elif fitness_p1 == fitness_p2:  # se derem iguais, escolho algum de forma aleatória
            aux = random.randint(1, 2)
            if aux == 1:
                #print("> P1 passa = ", fitness_p1)
                ganhadores.append(p1)
            else:
                #print("> P2 passa = ", fitness_p2)
                ganhadores.append(p2)
            # se os fitness são iguais então basta pegar qualquer um
            melhor_pai[0] = p1
            melhor_pai[1] = fitness_p1

    return ganhadores


def cruzamento():
    # rodo o cruzamento 15 vezes, pois cada par me gera 2 filhos
    for x in range(0, 30, 2):  # iteração começa em 0, vai até 30 e incrementa em 2
        # seleciona aleatoriamente dois pares de vencedores para serem cruzados
        v1 = v2 = 0
        while v1 == v2:
            v1 = random.randint(0, 29)
            v2 = random.randint(0, 29)

        pai_1 = vencedores[v1]
        pai_2 = vencedores[v2]

        #print("pai 1 = ", individuos[pai_1])
        #print("pai 2 = ", individuos[pai_2])

        # ponto de corte
        corte = random.randint(1, 8)
        #print("Corte = ", corte)

        # declaro dois filhos gerados no cruzamento
        filho_1 = []
        filho_2 = []

        # percorro a primeira parte
        for k in range(corte):
            filho_1.append(individuos[pai_1][k])
            filho_2.append(individuos[pai_2][k])

        # percorro a segunda parte
        for p in range(corte, len(individuos[pai_1])):
            filho_1.append(individuos[pai_2][p])
            filho_2.append(individuos[pai_1][p])

        # tenho dois filhos de um cruzamento
        filhos_cruzamento[x] = filho_1
        filhos_cruzamento[x + 1] = filho_2


def get_pior_filho():
    pior_filho = [100, 100]
    for x in range(30):
        pf = sinal_saida(int_pra_bin(filhos_cruzamento[x]))
        if pf < pior_filho[1]:
            pior_filho[1] = pf
            pior_filho[0] = x
    return pior_filho


def get_melhor_filho():
    melhor_filho = [0, 0]
    for x in range(30):
        pf = sinal_saida(int_pra_bin(filhos_cruzamento[x]))
        if pf > melhor_filho[1]:
            melhor_filho[1] = pf
            melhor_filho[0] = x
    return melhor_filho
# ----------------------------------------------------------------------------------------------------------------------


# matriz com 30 individuos com 9 elementos, preenchida com 0
individuos = np.zeros((30, 9), dtype=int)

# percorro cada elemento e adiciono um valor aleatório entre 0 e 15
for i in range(len(individuos)):
    print(i, " - ", end="")
    for j in range(len(individuos[i])):
        individuos[i][j] = random.randint(0, 15)
        print(individuos[i][j], " ", end="")
    print()

for i in range(40):
    # realizo o torneio binário e tenho um vetor com as posições dos vencedores la da matriz de individuos
    vencedores = torneio_binario()

    # matriz que irá guardar todos os filhos dos cruzamentos
    filhos_cruzamento = np.zeros((30, 9), dtype=int)

    # chama função para realizar os cruzamentos
    cruzamento()

    # obtenho o melhor pai e substituo pelo pior filho
    filho_ruim = get_pior_filho()
    filhos_cruzamento[filho_ruim[0]] = individuos[melhor_pai[0]]

    individuos = filhos_cruzamento

print(get_melhor_filho())

# -------------------------------------------------


# representação binária dos filhos e pais


'''
teste = '0111111111111111111111111111111111111'

print(sinal_saida(int_pra_bin(filho_1)))
print(sinal_saida(int_pra_bin(filho_2)))

print(individuos[vencedores[v1]])
print(individuos[vencedores[v2]])

print(sinal_saida(int_pra_bin(individuos[vencedores[v1]])))
print(sinal_saida(int_pra_bin(individuos[vencedores[v2]])))

'''
