def matCreate(n):
    matrix = []
    for i in range(0,n):
        matrix.append([])
        for j in range(0,n):
            matrix[i].append(0)
    return matrix

def matPrint(matrix):
    l = len(matrix)
    print("  ",end="")
    for i in range(0,l):
        print(str(i)+" ",end="")
    print("")
    for i in range(0,l):
        print(str(i)+"|",end="")
        for j in range(0,l-1):
            print(str(matrix[i][j])+" ",end="")
        print(str(matrix[i][l-1])+"|")

def vNome(name,m):
    for i in range(0,len(m)):
        if name == m[i][0]:
            return i
    return -1
    
print("Comandos: ler, add")
matrices = []
while True:
    opt = input("Deseja ler ou adicionar uma matriz? ")
    if opt == "ler":
        num = vNome(input("Digite o nome do grafo: "),matrices)
        if num >= 0:
            matPrint(matrices[num][1])
        else:
            print("Grafo nao encontrado.")
    elif opt == "add":
        n = int(input("Digite n: "))
        while n <= 0:
            n = int(input("Numero invalido, digite outro: "))
        m = int(input("Digite m: "))
        cont2 = 0
        for i in range(0,n):
            for j in range(i+1,n):
                cont2 += 1
        while m < 0 or m > cont2:
            m = int(input("Numero invalido, digite outro: "))
        cont = 0
        print("Digite 1 para adjacencia")
        print("Digite outro caracter para nao adjacencia")
        matrix = matCreate(n)
        for i in range(0,n):
            for j in range(0,n):
                if j >= i+1 and cont < m:
                    if cont2 == m:
                        matrix[i][j] = "1"
                        matrix[j][i] = "1"
                        continue
                    adj = input(str(i)+"-"+str(j)+": ")
                    if adj == "1":
                        matrix[i][j] = adj
                        matrix[j][i] = adj
                        cont += 1
                    cont2 -= 1
        nome = input("Qual nome deseja dar ao grafo? ")
        while vNome(nome,matrices) >= 0:
            nome = input("Nome ja em uso, digite outro: ")
        matrices.append([nome,matrix])
    else:
        print("Opcao invalida")

