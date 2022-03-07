import numpy as np
import random

''' ATUALIZAÇÕES

    1) Os pais devem ser calculados com o fitness, que é a função sinal_saida(). 
    Então a função deve ser chamada logo aqui no começo.

    2) A mutação de 0,03 é basicamente 3%, ou seja, num sorteiro aleatório entre
    1 e 100, se sair os números 1, 2 ou 3 a mutação ocorre. Feito isso para cada 
    indivíduo basta selecionar um bit dele e alterar.

    3) 
'''


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


# matriz com 30 individuos com 9 elementos, preenchida com 0
individuos = np.zeros((30, 9), dtype=int)

# percorro cada elemento e adiciono um valor aleatório entre 0 e 15
for i in range(len(individuos)):
    print(i, " - ", end="")
    for j in range(len(individuos[i])):
        individuos[i][j] = random.randint(0, 15)
        print(individuos[i][j], " ", end="")
    print()


# declaro uma lista vazia para guardar os vencedores do torneio
vencedores = []

# realizo o torneio entre 10 pares de indivíduos
for a in range(30):

    # escolho dois individuos de forma aleatória
    p1 = p2 = 0
    while p1 == p2:
        p1 = random.randint(0, 29)
        p2 = random.randint(0, 29)

    # faço um torneio binário entre p1 e p2
    soma_p1 = soma_p2 = 0

    for k in range(len(individuos[p1])):
        soma_p1 = soma_p1 + individuos[p1][k]  # soma de p1

    for k in range(len(individuos[p2])):
        soma_p2 = soma_p2 + individuos[p2][k]  # soma de p2

    # quem for maior passa no torneio
    if soma_p1 > soma_p2:
        print("P1 passa = ", soma_p1)
        vencedores.append(p1)
    elif soma_p1 < soma_p2:
        print("P2 passa = ", soma_p2)
        vencedores.append(p2)
    elif soma_p1 == soma_p2:  # se derem iguais, escolho algum de forma aleatória
        aux = random.randint(1, 2)
        if aux == 1:
            print("> P1 passa = ", soma_p1)
            vencedores.append(p1)
        else:
            print("> P2 passa = ", soma_p2)
            vencedores.append(p2)

print(vencedores)

# seleciona aleatoriamente dois pares de vencedores para serem cruzados
v1 = v2 = 0
while v1 == v2:
    v1 = random.randint(0, 29)
    v2 = random.randint(0, 29)

print("pai 1 = ", individuos[vencedores[v1]])
print("pai 2 = ", individuos[vencedores[v2]])

# ponto de corte
corte = random.randint(1, 8)
print("Corte = ", corte)

# declaro dois filhos gerados no cruzamento
filho_1 = []
filho_2 = []

# percorro a primeira parte
for k in range(corte):
    filho_1.append(individuos[vencedores[v1]][k])
    filho_2.append(individuos[vencedores[v2]][k])

# percorro a segunda parte
for p in range(corte, len(individuos[vencedores[v1]])):
    filho_1.append(individuos[vencedores[v2]][p])
    filho_2.append(individuos[vencedores[v1]][p])

# tenho dois filhos de um cruzamento
print(filho_1)
print(filho_2)
# -------------------------------------------------



# representação binária dos filhos e pais


print(sinal_saida(int_pra_bin(filho_1)))
print(sinal_saida(int_pra_bin(filho_2)))

print(individuos[vencedores[v1]])
print(individuos[vencedores[v2]])

print(sinal_saida(int_pra_bin(individuos[vencedores[v1]])))
print(sinal_saida(int_pra_bin(individuos[vencedores[v2]])))

'''
teste = '0111111111111111111111111111111111111'


'''
