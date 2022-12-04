def drawGraphs():
    import networkx as nx
    import matplotlib.pyplot as plt
    for row in matrices:
        G = nx.DiGraph() 
        for i in range(0,len(row[1])):
            for j in range(0,len(row[1])):
                if row[1][i][j] == 1:
                    G.add_edge(i,j)
        nx.draw(G)
        plt.savefig("graph{}.png".format(row[0]))
        plt.clf()
    
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
        
def numRestrict(name = "n", restrictions = [0], comp = [1]):
    n = int(input("Digite {}: ".format(name)))
    notValid = True
    while notValid:
        notValid = False
        for i,j in enumerate(restrictions):
            if not comp[i]*j < comp[i]*n:
                notValid = True
        if notValid:
            n = int(input("Valor invalido, digite outro: "))
    return n

def findNome(name):
    names = [row[0] for row in matrices]
    if name in names: return names.index(name)
    return -1

def lerMat():
    num = findNome(input("Digite o nome do grafo: "))
    if num >= 0: matPrint(matrices[num][1])
    else: print("Grafo nao encontrado.")

def listMat():
    for i in matrices:
        print(i[0])

def addMat():
    n = numRestrict()
    matrix = [[0 for j in range(0,n)] for i in range(0,n)]
    mAvaliable = sum(n-i-1 for i in range(0,n))
    m = numRestrict("m",[-1,mAvaliable+1],[1,-1])
    print("[1]: Adjacencia")
    print("[0]: N Adjacencia")
    for i in range(0,n):
        for j in range(i+1,n):
            if m == 0: break
            if mAvaliable == m:
                matrix[i][j], matrix[j][i] = 1,1
                continue
            adj = input(str(i)+"-"+str(j)+": ")
            while adj != "0" and adj != "1":
                adj = int(input("Opcao invalida, digite outra: "))
            if adj == "1":
                matrix[i][j], matrix[j][i] = 1,1
                m -= 1
            mAvaliable -= 1
    saveGraph(matrix)
    
def cubeGraph(n):
    if n == 0: return [[0]]
    cube = cubeGraph(n-1)
    mat = [[1 if j == i else 0
            for j in range(0,len(cube))]
            for i in range(0,len(cube))]
    conc1 = [cube[i]+mat[i]
            for i in range(0,len(mat))]
    conc2 = [mat[i]+cube[i]
            for i in range(0,len(mat))]
    return conc1+conc2

def addGraph():
    types = ["Completo","BipartidoCompleto","Estrela",
             "Ciclo","Roda","Caminho","Cubo"]
    options = "abcdefg"
    for i,j in enumerate(options):
        print("({}){}".format(j,types[i]))
    opt = input("Digite sua opcao: ")
    while opt not in options:
        opt = input("Opcao invalida, digite outra: ")
    graphs(opt, types[options.index(opt)])
    
def graphs(opt,name):
    if opt == "a":
        n = numRestrict()
        saveGraph([[1 if j != i else 0
                 for j in range(0,n)]
                 for i in range(0,n)],
                 name+"$n"+str(n)+"$")
    elif opt == "b":
        n1 = numRestrict("n1")
        n2 = numRestrict("n2")
        saveGraph([[1 if ((j>=n1 and i<n1)
                 or (j<n1 and i>=n1))
                 and (j != i) else 0
                 for j in range(0,n1+n2)]
                 for i in range(0,n1+n2)],
                 name+"$n"+str(n1)+"$n"+str(n2)+"$")
    elif opt == "c":
        n = numRestrict()+1
        saveGraph([[1 if (j == n//2 or i == n//2)
                 and (j != i) else 0
                 for j in range(0,n)]
                 for i in range(0,n)],
                 name+"$n"+str(n-1)+"$")
    elif opt == "d":
        n = numRestrict(restrictions = [2])
        saveGraph([[1 if j == i+1 or j == i-1
                 or (j == 0 and i == n-1)
                 or (j == n-1 and i == 0) else 0
                 for j in range(0,n)]
                 for i in range(0,n)],
                 name+"$n"+str(n)+"$")
    elif opt == "e":
        n = numRestrict()
        mat = [[1 if j == i+1 or j == i-1 or (j == 0 and i == n-1)
                 or (j == n-1 and i == 0) else 0
                 for j in range(0,n)]
                 for i in range(0,n)]
        for i in mat:
            i.insert(n//2,1)
        arr = [0 if i == n//2 else 1 for i in range(0,n+1)]
        mat.insert(n//2,arr)
        saveGraph(mat,name+"$n"+str(n)+"$")
    elif opt == "f": 
        n = numRestrict()
        saveGraph([[1 if j == i+1 or i == j+1 else 0
                 for j in range(0,n)]
                 for i in range(0,n)],name+"$n"+str(n)+"$")   
    elif opt == "g":
        n = numRestrict(restrictions = [-1])
        saveGraph(cubeGraph(n),name+"$n"+str(n)+"$")

def loadGraphs():
    mat = []
    from os.path import exists
    if exists("names.txt"):
        file = open("names.txt")
        for i in file:
            if exists(str(i).strip()+".txt"):
                files = open(str(i).strip()+".txt","r")
                mat2 = []
                for j in files:
                    mat2.append([int(i) for i in j.strip().split(", ")])
                mat.append([str(i).strip(),mat2])
                files.close()
        file.close()
    return mat

def saveGraph(matrix, nome = False):
    if nome == False:
        nome = input("Qual nome deseja dar ao grafo? ")
        while findNome(nome) >= 0:
            nome = input("Nome ja em uso, digite outro: ")
    file = open(nome+".txt","w")
    for i in matrix:
        file.write(", ".join(str(j) for j in i))
        file.write("\n")
    file.close()
    if findNome(nome) < 0:
        file2 = open("names.txt","a+")
        file2.write(nome+"\n")
        file2.close()
        matrices.append([nome,matrix])

def matToAdjList(matrix):
    arr = []
    for i in matrix:
        adj = [j for j in range(0,len(i)) if i[j] == 1]
        arr.append(adj)
    return arr

def buscaEmLargura():
    num = findNome(input("Digite o nome do grafo: "))
    if num < 0:
        print("Grafo nao encontrado.")
        return
    adjList = matToAdjList(matrices[num][1])
    visited = []
    cont = 0
    for vI,_ in enumerate(adjList):
        if vI in visited: continue
        queue = [vI]
        while len(queue) > 0:
            v = queue.pop(0)
            if v not in visited:
                visited.append(v)
                queue += set(adjList[v]).difference(visited)
        cont+= 1
    print("O grafo possui {} componente(s)".format(cont))

print("Carregando grafos...")
matrices = loadGraphs()
listMat()
print("Comandos: ler, listar, addM, addG, nComp, fim")
while True:
    opt = input("O que deseja fazer? ")
    if opt == "ler": lerMat()
    elif opt == "listar": listMat()
    elif opt == "addM": addMat()
    elif opt == "addG": addGraph()
    elif opt == "nComp": buscaEmLargura()
    elif opt == "secret": drawGraphs()
    elif opt == "fim": break
    else: print("Opcao invalida.")
print("Fim do programa.")
