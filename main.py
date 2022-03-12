import numpy as np
import random
import matplotlib.pyplot as plt

# VARIÁVEIS GLOBAIS
ganhadores = []  # Usado no torneio binário. Lista para guardar os vencedores do torneio
individuos_bin = np.zeros((30, 36), dtype=int)  # Usado na conversão da matriz individuos, int pra binário


# Função que vai preencher a matriz de indivíduos com valores aleatórios.
def gera_individuos():
    # percorro cada elemento e adiciono um valor aleatório entre 0 e 15
    for x in range(len(individuos)):
        for y in range(len(individuos[x])):
            individuos[x][y] = random.randint(0, 15)


# Função que converte a matriz de individuos para outra matriz com os valores binários.
def converte_pra_bin():
    for x in range(len(individuos)):
        individuos_bin[x] = int_pra_bin(individuos[x])


# Função que converte inteiro para binário, onde cada bit é um caractere char.
def int_pra_bin(vet_int):
    vet_char_bin = ''
    vet_int_bin = []

    for x in range(len(vet_int)):
        num_bin = "{0:{fill}4b}".format(vet_int[x], fill='0')  # converte o inteiro em binário, 4 bits
        vet_char_bin += num_bin  # salvo cada bit como um caractere

    for y in range(len(vet_char_bin)):  # converto o vetor de caractere gerado para um vetor de int
        if vet_char_bin[y] == '1':
            vet_int_bin.append(1)
        else:
            vet_int_bin.append(0)
    return vet_int_bin


# Função fitness, que transforma os valores em binário para um valor inteiro.
def funcao_fitness(v):
    r = (9 + (int(v[1]) * int(v[4])) - (int(v[22]) * int(v[13]))
         + (int(v[23]) * int(v[3])) - (int(v[20]) * int(v[9]))
         + (int(v[35]) * int(v[14])) - (int(v[10]) * int(v[25]))
         + (int(v[15]) * int(v[16])) + (int(v[2]) * int(v[32]))
         + (int(v[27]) * int(v[18])) + (int(v[11]) * int(v[33]))
         - (int(v[30]) * int(v[31])) - (int(v[21]) * int(v[24]))
         + (int(v[34]) * int(v[26])) - (int(v[28]) * int(v[8]))
         + (int(v[7]) * int(v[14])) - (int(v[5]) * int(v[8]))
         + (int(v[17]) * int(v[19])) - (int(v[0]) * int(v[29]))
         + (int(v[22]) * int(v[3])) + (int(v[20]) * int(v[14]))
         + (int(v[25]) * int(v[15])) + (int(v[30]) * int(v[11]))
         + (int(v[24]) * int(v[18])) + (int(v[6]) * int(v[7]))
         + (int(v[8]) * int(v[17])) + (int(v[0]) * int(v[32])))
    return r


# Função que realiza o torneio binário, retornando um vetor com as posições
# na matriz de individuos referente aos vencedores do torneio.
def torneio_binario():
    # realizo o torneio 30 vezes para manter 30 indivíduos
    for x in range(len(individuos)):

        # escolho dois individuos de forma aleatória, que não seja o mesmo
        p1 = p2 = 0
        while p1 == p2:
            p1 = random.randint(0, len(individuos) - 1)
            p2 = random.randint(0, len(individuos) - 1)

        # faço um torneio binário entre p1 e p2
        fitness_p1 = funcao_fitness(individuos_bin[p1])
        fitness_p2 = funcao_fitness(individuos_bin[p2])

        # quem for maior passa no torneio
        if fitness_p1 > fitness_p2:
            ganhadores.append(p1)

        elif fitness_p1 < fitness_p2:
            ganhadores.append(p2)

        else:  # fitness_p1 == fitness_p2 Se derem iguais, escolho algum de forma aleatória
            aux = random.randint(1, 2)
            if aux == 1:
                ganhadores.append(p1)
            else:
                ganhadores.append(p2)


def torneio_roleta():
    # realizo o torneio 30 vezes para manter 30 indivíduos
    for x in range(len(individuos)):

        vet_fitness = []  # vetor que guarda o fitness de cada indivíduo
        soma_fitness = 0  # guarda a soma total dos fitness, que representa 100% da roleta
        fit_relativo = []  # guarda o valor fitness relativo

        # calculo o fitness de cada individuo
        for y in range(len(individuos)):
            vet_fitness.append(funcao_fitness(individuos_bin[y]))
            soma_fitness += vet_fitness[y]

        for y in range(len(vet_fitness)):
            fit_relativo.append(round((vet_fitness[y] * 100) / soma_fitness))  # faço arredondamento pro teto ou chão

        # A roleta representa uma sequência de 1 até 100,
        # cada valor dentro de fit_relativo representa quantos
        # números da sorte ele possui. Se o primeiro valor (fit_relativo[0])
        # fosse 3, por exemplo, então ele tem os números 1, 2 e 3. Se o próximo
        # valor (fit_relativo[1]) fosse 4, então ele tem os números 4, 5, 6 e 7.
        # Dessa forma, se o 'n' for 6, quem é selecionado é o indivíduo
        # com fit_relativo de valor 4.
        n = random.randint(0, 100)
        aux = 0
        for y in range(len(fit_relativo)):
            if aux < n <= (fit_relativo[y] + aux):
                ganhadores.append(y)
            else:
                aux += fit_relativo[y]


# Função que irá cruzar dois pais para gerar dois filhos.
def cruzamento():
    # rodo o cruzamento 15 vezes, pois cada par me gera 2 filhos
    for x in range(0, len(individuos_bin), 2):  # iteração começa em 0, vai até 30 e incrementa em 2

        # gero dois pares de vencedores para serem cruzados
        v1 = v2 = 0
        while v1 == v2:
            v1 = random.randint(0, len(individuos_bin) - 1)
            v2 = random.randint(0, len(individuos_bin) - 1)

        pai_1 = ganhadores[v1]
        pai_2 = ganhadores[v2]

        # ponto de corte gera um valor vezes 4, pois o valor binário está representado com 4 bits
        corte = random.randint(1, 8) * 4

        # declaro dois filhos gerados no cruzamento
        filho_1 = []
        filho_2 = []

        # percorro a primeira parte
        for k in range(corte):
            filho_1.append(individuos_bin[pai_1][k])
            filho_2.append(individuos_bin[pai_2][k])

        # percorro a segunda parte
        for p in range(corte, len(individuos_bin[pai_1])):  # começo do corte e vou até o final do vetor
            filho_1.append(individuos_bin[pai_2][p])
            filho_2.append(individuos_bin[pai_1][p])

        # tenho dois filhos de um cruzamento
        filhos_cruzamento[x] = filho_1
        filhos_cruzamento[x + 1] = filho_2


# Função que vai realizar a mutação, ou seja, invertendo o valor de um bit.
def mutacao():
    filho_mutado = random.randint(0, len(individuos_bin) - 1)
    posicao_bit = random.randint(0, 35)

    bit = filhos_cruzamento[filho_mutado][posicao_bit]

    if bit == '1':
        filhos_cruzamento[filho_mutado][posicao_bit] = '0'
    else:
        filhos_cruzamento[filho_mutado][posicao_bit] = '1'


# Função que determina se haverá mutação em função das taxas de 0.03, 0.05, 0.1 e 0.4,
# que correspondem a 3%, 5%, 10% e 40%.
def taxa_mutacao(porcentagem):
    valor = random.randint(1, 100)
    mut = False

    if porcentagem == 3:
        if 0 < valor <= 3:
            mut = True
    elif porcentagem == 5:
        if 0 < valor <= 5:
            mut = True
    elif porcentagem == 10:
        if 0 < valor <= 10:
            mut = True
    elif porcentagem == 40:
        if 0 < valor <= 40:
            mut = True
    else:
        mut = False
    return mut


# Função que percorre toda matriz de filhos gerados pelo cruzamento,
# calcula o fitness de cada um e retorna quem tem o pior valor.
def get_pior_filho():
    pior_filho = [0, 100]
    for x in range(len(filhos_cruzamento)):
        fit = funcao_fitness(filhos_cruzamento[x])
        if fit < pior_filho[1]:
            pior_filho[0] = x
            pior_filho[1] = fit
    return pior_filho


# Função que percorre toda matriz de individuos, ou seja, os pais,
# calcula o fitness de cada um e retorna quem tem o melhor valor.
def get_melhor_pai():
    melhor_pai = [0, 0]
    for x in range(len(individuos_bin)):
        fit = funcao_fitness(individuos_bin[x])
        if fit > melhor_pai[1]:
            melhor_pai[0] = x
            melhor_pai[1] = fit
    return melhor_pai


# ----------------------------------------------------------------------------------------------------------------------


m = 0
melhor = 0
contador = 0
data = []
qtd_melhor = 0

while melhor != 27 and contador < 10:

    # matriz com 30 individuos com 9 elementos, preenchida com 0
    individuos = np.zeros((30, 9), dtype=int)

    # gera um valor aleatório para cada indivíduo
    gera_individuos()

    # converter os valores gerados na matriz individuos para binário
    converte_pra_bin()

    for i in range(40):
        # realizo o torneio e tenho um vetor com as posições dos vencedores la da matriz de individuos
        torneio_binario()
        # torneio_roleta()

        # matriz que irá guardar todos os filhos dos cruzamentos
        # [['' for i in range(30)] for j in range(36)]
        filhos_cruzamento = np.zeros((30, 36), dtype=int)

        # chama função para realizar os cruzamentos e preencher a matriz criada acima, já em binário
        cruzamento()

        # determino a taxa de mutação
        if taxa_mutacao(10):
            mutacao()

        # obtenho o melhor pai e substituo pelo pior filho
        pf = get_pior_filho()
        mp = get_melhor_pai()
        filhos_cruzamento[pf[0]] = individuos_bin[mp[0]]

        # a população de filhos substitui a população de pais
        individuos_bin = filhos_cruzamento

        m = get_melhor_pai()
        if m[1] >= melhor:
            melhor = m[1]
            print(i, " - ", melhor)
    print("\nking - ", melhor)
    contador += 1
    data.append(melhor)

fig = plt.figure(figsize=(8, 5))

# Creating axes instance
# ax = fig.add_axes([0, 0, 1, 1])

# Creating plot
# bp = ax.boxplot(data)

plt.boxplot(data)
# show plot
plt.show()
