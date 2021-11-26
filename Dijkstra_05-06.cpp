#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <tuple>
#include <stdexcept>
#include <sstream>
#include <stdio.h>
#define inf 10000000.0
using namespace std;

struct antecessor{
	int no;
	bool existe;
	antecessor *ant;
};

class Grafo{
private:
	int V; 
	list<pair<int, double> > * adj; 
public:
	Grafo(int V){
		this->V = V; 
		adj = new list<pair<int, double> >[V]; 
	}
	void addAresta(int v1, int v2, double peso){
		adj[v1].push_back(make_pair(v2, peso)); 
	}
	
	list<int> dijkstra(int orig, int dest){
		double dist[V]; 
		int visitado[V]; 
		priority_queue < pair<double, int>, 
		vector<pair<double, int>>, greater<pair<double, int>> > pq;
		for(int i = 0; i < V; i++){dist[i] = inf; visitado[i] = false;} dist[orig] = 0.0;
		pq.push(make_pair(dist[orig], orig)); 
		antecessor antecessores[V]; 
		for (int i = 0; i < V; i++){
			antecessores[i].no = i; 
			antecessores[i].existe = 0;
		} 
		while(!pq.empty()){
			pair<double,int> p = pq.top(); 
			int u = p.second;
			pq.pop(); 
			if(visitado[u] == false){
				visitado[u] = true;
				list<pair<int, double>>::iterator it;
				for(it = adj[u].begin(); it != adj[u].end(); it++){
					int v = it->first; 
					double peso_aresta = it->second; 
					if(dist[v] > (dist[u] + peso_aresta)){
						antecessores[v].ant = &(antecessores[u]);
						antecessores[v].existe = 1;
						dist[v] = dist[u] + peso_aresta; 
						pq.push(make_pair(dist[v], v)); 
					}
				}
			}
		}
		cout << endl << "Inicio: " << orig << ' ' << "Destino: " << dest << endl;
		list<int> caminho; int x = dest;
		
		while (antecessores[x].no != orig){
			caminho.insert(caminho.begin(), antecessores[x].no); 
			if (antecessores[x].existe) x = antecessores[x].ant->no;
			else{
				printf("Menor caminho nao encontrado... :(");
				return {};
			}
		}
		caminho.insert(caminho.begin(), antecessores[x].no);
		printf("Menor caminho encontrado! \nDistancia: %f\nCaminho: ", dist[dest]);
		return caminho;
	}
};

void ImprimeCaminho(Grafo g, int a, int b){
	list<int> mcaminho = g.dijkstra(a,b);
	list<int>::iterator cont;
	for (cont = mcaminho.begin(); cont != mcaminho.end(); ++cont){
    	cout << *cont << ' ';
	} cout << endl << endl;
}

int contNumNodes(){
	ifstream myFile("Nodes.csv"); string line; int lines;
	if(!myFile.is_open()){throw runtime_error("Could not open Nodes");}
	for(lines = 0; getline(myFile,line); lines++);
	myFile.close();
	return lines;
}

Grafo LeArquivo(){
	ifstream nodes("Edges.csv"); double val; int x[4]; double z; int y; string line;
	int a = contNumNodes(); Grafo g(a);
    if(!nodes.is_open()){throw runtime_error("Could not open Edges");}
    if(nodes.good()){
    	while(getline(nodes, line)){
	        stringstream ss(line);
	        y = 0;
	        while(ss >> val){
				if (y != 2) x[y] = val;
				else z = val;
	       		if(ss.peek() == ',') ss.ignore();
	       		y++;
	       	}
	       	g.addAresta(x[0],x[1], z);
			if (x[3] == 0) g.addAresta(x[1],x[0], z);
		}
    } nodes.close();
    return g;
}

int main(int argc, char *argv[]){
	Grafo rj = LeArquivo();
	while(true){
		int a; printf("Digite o no inicial: "); scanf("%d",&a);
		int b; printf("Digite o no final: "); scanf("%d",&b);
		ImprimeCaminho(rj, a, b);
	}
	return 0;
}
