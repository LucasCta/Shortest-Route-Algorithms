#Gera Imagens dos Grafos
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
        plt.savefig("graphs\graph{}.png".format(row[0]))
        plt.clf()

#Função Auxiliar para Restringir Valores
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

#Verifica se a Matriz Existe
def findNome(name):
    names = [row[0] for row in matrices]
    if name in names: return names.index(name)
    return -1

#Printa uma Matriz
def matPrint():
    num = findNome(input("Digite o nome do grafo: "))
    matrix = matrices[num][1]
    if num >= 0:
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
    else: print("Grafo nao encontrado.")

#Lista as Matrizes Geradas
def listMat():
    for i in matrices:
        print(i[0])

#Gera uma Matriz Personalizada
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

#Mostra as Opções de Grafos Conhecidos
def addGraph():
    types = ["Completo","BipartidoCompleto","Estrela",
             "Ciclo","Roda","Caminho","Cubo","Mycielski"]
    options = "abcdefgh"
    for i,j in enumerate(options):
        print("({}){}".format(j,types[i]))
    opt = input("Digite sua opcao: ")
    while opt not in options:
        opt = input("Opcao invalida, digite outra: ")
    graphs(opt, types[options.index(opt)])

#Gera Matrizes de Grafos Conhecidos
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
        n = numRestrict(restrictions = [-1])
        saveGraph(cubeGraph(n),name+"$n"+str(n)+"$")
    elif opt == "h":
        def Mycielsky(matrix,n,X):
            if n == X:
                return matrix
            else:
                nMatrix = []
                for i in matrix:
                    nMatrix.append(i+i+[0])
                for i in matrix:
                    nMatrix.append(i+[0 for i in range(0,len(matrix))]+[1])
                nMatrix.append([0 for i in range(0,len(matrix))]+
                               [1 for i in range(0,len(matrix))]+
                               [0])
                return Mycielsky(nMatrix,n+1,X)
        w = numRestrict("w",restrictions = [2-1])
        matrix = [[1 if j != i else 0
                 for j in range(0,w)]
                 for i in range(0,w)]
        X = numRestrict("X",restrictions = [w-1])
        saveGraph(Mycielsky(matrix,w,X),
                  name+"$w"+str(w)+"X"+str(X)+"$")
        
#Carrega as Matrizes da Memória
def loadGraphs():
    mat = []
    from os.path import exists
    if exists("graphs/names.txt"):
        file = open("graphs/names.txt")
        for i in file:
            if exists("graphs/"+str(i).strip()+".txt"):
                files = open("graphs/"+str(i).strip()+".txt","r")
                mat2 = []
                for j in files:
                    mat2.append([int(i) for i in j.strip().split(", ")])
                mat.append([str(i).strip(),mat2])
                files.close()
        file.close()
    return mat

#Salva as Matrizes na Memória
def saveGraph(matrix, nome = False):
    if nome == False:
        nome = input("Qual nome deseja dar ao grafo? ")
        while findNome(nome) >= 0:
            nome = input("Nome ja em uso, digite outro: ")
    file = open("graphs/"+nome+".txt","w")
    for i in matrix:
        file.write(", ".join(str(j) for j in i))
        file.write("\n")
    file.close()
    if findNome(nome) < 0:
        file2 = open("graphs/names.txt","a+")
        file2.write(nome+"\n")
        file2.close()
        matrices.append([nome,matrix])

#Transforma uma Matriz em uma Lista de Adjacência
def matToAdjList(matrix):
    arr = []
    for i in matrix:
        adj = [j for j in range(0,len(i)) if i[j] == 1]
        arr.append(adj)
    return arr

#Algoritmo de Busca em Largura / Verificar Euleriano
def buscaEmLargura(opt):
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
    if not opt:
        print("O grafo possui {} componente(s)".format(cont))
    else:
        for v in adjList:
            if len(v)%2 != 0:
                print("O grafo não é Euleriano")
                renum = findNome(input("Digite o nome do grafo: "))
    if num < 0:
        print("Grafo nao encontrado.")
        returnturn
        print("O grafo é Euleriano")

#Algoritmo de Busca em Profundidade
def buscaEmProfundidade(opt):
    num = findNome(input("Digite o nome do grafo: "))
    if num < 0:
        print("Grafo nao encontrado.")
        return
    aL = matToAdjList(matrices[num][1])
    cpre = 0
    pre = [0 for i in aL] 
    low = [0 for i in aL] 
    pA, pM = [], []
    inicio = int(input("Digite o v inicial: "))-1
    priorityList = list(range(inicio,len(aL))) + list(range(0,inicio))
    for v in priorityList:
    	if pre[v] == 0:
    		if opt == 0: 
    		    pre, cpre = DFS(v,aL,pre,cpre)
    		elif opt == 1: 
    		    pre, cpre, low = Pontes(v,v,aL,pre,cpre,low)	
    		elif opt == 2: 
    		    pre, cpre, low, pA, pM = Biconexo(v,v,aL,pre,cpre,low,pA,pM)
    
def DFS(v,aL,pre,cpre):
    cpre += 1
    pre[v] = cpre
    print (pre)
    for i in aL[v]:
        if pre[i] == 0:
            pre, cpre = DFS(i,aL,pre,cpre)
    return pre, cpre
       
def Pontes(p,v,aL,pre,cpre,low):
    cpre += 1
    pre[v] = cpre
    low[v] = cpre
    print ("Entrando em ", v+1, " -> pre:", pre, "low:", low)
    for i in aL[v]:
        if pre[i] == 0:
            pre, cpre, low = Pontes(v,i,aL,pre,cpre,low)
            if low[i] == pre[i]:
                print("Ponte encontrada: {}-{}".format(v+1,i+1))
            low[v] = min(low[v], low[i])
        elif i != p:
            low[v] = min(low[v], pre[i])
    print ("Saindo de ", v+1, "   -> pre:", pre, "low:", low)
    return pre, cpre, low
    
def Biconexo(p,v,aL,pre,cpre,low,pA,pM):
    cpre += 1
    pre[v] = cpre
    low[v] = cpre
    print ("Entrando em ", v+1, " -> pre:", pre, "low:", low)
    for i in aL[v]:
        aresta = ["{}-{}".format(min(i+1,v+1),max(i+1,v+1))]
        if aresta not in pA and aresta not in pM:
            pM.append(aresta)
            pA.append(aresta)
        if pre[i] == 0:
            pre, cpre, low, pA, pM = Biconexo(v,i,aL,pre,cpre,low,pA,pM)
            if pre[v] <= low[i]:
                print ("Componente Biconexo: ",end="")
                while pA[len(pA)-1] != aresta:
                    print(pA.pop(),end="")
                print(pA.pop())
            low[v] = min(low[v], low[i])
        elif i != p:
	        low[v] = min(low[v], pre[i])
    print ("Saindo de ", v+1, "   -> pre:", pre, "low:", low)
    return pre, cpre, low, pA, pM
	
    
#Retorna Coloração Gulosa dos Vértices
def coloracaoGulosa():
    num = findNome(input("Digite o nome do grafo: "))
    if num < 0:
        print("Grafo nao encontrado.")
        return
    mat = matrices[num][1]
    for i in mat:
        i.append("0")
    for i in mat:
        usedColors = {"0"}
        for j in range(0,len(i)-1):
            if i[j] == 1:
                usedColors.add(mat[j][len(i)-1])
        color = 0
        while str(color) in usedColors:
            color += 1
        i[len(i)-1] = str(color)
        print(color,end="")
    print("")

def Programa():
    print("Carregando grafos...")
    listMat()
    while True:
        print("Comandos: ler, list, color, addM, addG, nComp, euler, DFS, ponte, biconexo, fim")
        opt = input("O que deseja fazer? ")
        if opt == "ler": matPrint()
        elif opt == "list": listMat()
        elif opt == "addM": addMat()
        elif opt == "addG": addGraph()
        elif opt == "nComp": buscaEmLargura(0)
        elif opt == "color": coloracaoGulosa()
        elif opt == "euler": buscaEmLargura(1)
        elif opt == "secret": drawGraphs()
        elif opt == "DFS": buscaEmProfundidade(0)
        elif opt == "ponte": buscaEmProfundidade(1)
        elif opt == "biconexo": buscaEmProfundidade(2)
        elif opt == "fim": break
        else: print("Opcao invalida.")
    print("Fim do programa.")

matrices = loadGraphs()
Programa()
