#include <iostream>
#include <fstream>
#include <list>
#include <queue>
#include <tuple>
#include <stdexcept>
#include <sstream>
#include <stdio.h>
#include <cmath>
#define inf 1000000.0
using namespace std;
struct no{
	bool closed;
	double originDist;
	double heuristicDist;
	double fDistance;
	int antNo;
};
class Grafo{
private:
	int V; 
	list<pair<int, double>> * adj;
	pair<double,double> * latlon; 
public:
	Grafo(int V){
		this->V = V; 
		latlon = new pair<double,double>[V];
		adj = new list<pair<int, double>>[V]; 
	}
	void addLatLong(double lat, double lon, int cont){
		latlon[cont] = make_pair(lat, lon); 
	}
	void addAresta(int v1, int v2, double peso){
		adj[v1].push_back(make_pair(v2, peso)); 
	}
	list<int> AAsterisco(int orig, int dest){
		no *Rio; Rio = new no[V]; 
		//Calculates The Heuristic Distance
		double triangulo[3];  
		for (int i = 0; i < V; i++){
			triangulo[0] = (latlon[i].first - latlon[dest].first);
			triangulo[1] = (latlon[i].second - latlon[dest].second);
			triangulo[2] = hypot(triangulo[0],triangulo[1]);
			Rio[i].heuristicDist = triangulo[2];
		}
		//Sets Other General Struct Values
		for (int i = 0; i < V; i++){
			Rio[i].closed = false;
			Rio[i].originDist = inf;
		} Rio[orig].originDist = 0;
		//A* Algorithm
		list<int> pList; list<int>::iterator pl; pList.insert(pList.begin(),orig);
		while (pList.size() > 0){
			pl = pList.begin(); int curr = *pl; 
			list<pair<int, double>>::iterator it;
			for(it = adj[curr].begin(); it != adj[curr].end(); it++){
				int adjacente = it->first;
				if(Rio[adjacente].closed) continue;
				double lenght = Rio[curr].originDist + it->second;
				if (adjacente == dest){
					Rio[dest].antNo = curr;
					Rio[dest].originDist = lenght;
					list<int> caminho; int x = dest;
					while (Rio[x].antNo != orig){
						caminho.insert(caminho.begin(), x);
						x = Rio[x].antNo; 
					} caminho.insert(caminho.begin(), x);
					caminho.insert(caminho.begin(), orig);
					cout << endl << "Inicio: " << orig << ' ' << "Destino: " << dest << endl;
					printf("Menor Caminho Encontrado!");
					printf("\nDistancia: %f\nCaminho: ",Rio[dest].originDist);
					return caminho;
				} 
				if (Rio[adjacente].originDist > lenght){
					Rio[adjacente].originDist = lenght;
					Rio[adjacente].fDistance = Rio[curr].originDist + Rio[curr].heuristicDist;
					Rio[adjacente].antNo = curr;
					list<int>::iterator cont; bool nTerminou = true;
					for (cont = pList.begin(); cont != pList.end(); ++cont){
						if(Rio[*cont].fDistance > Rio[adjacente].fDistance){
							pList.insert(cont, adjacente);
							nTerminou = false;
							break;
						}
					} if (nTerminou) pList.insert(pList.end(), adjacente);
				} 
			} 
			Rio[curr].closed = true;
			pList.pop_front();
		}
		list<int> caminho; int x = dest;
		puts("Caminho nao Encontrado...");
		return caminho;
	}
};
void EncontraCaminho(Grafo g, int a, int b){
	list<int> mcaminho = g.AAsterisco(a,b); list<int>::iterator cont;
	for (cont = mcaminho.begin(); cont != mcaminho.end(); ++cont){
    	cout << *cont << ' ';
	} cout << endl << endl;
}
Grafo LeArquivo(){
	ifstream myFile("Nodes.csv"); string ling; int c;
	if(!myFile.is_open()){throw runtime_error("Could not open Nodes.csv");}
	for(c = 0; getline(myFile,ling); c++); myFile.close(); Grafo g(c);
	ifstream nodes("Edges.csv"); double val; int x[4]; double z; int y; string line;
    if(!nodes.is_open()){throw runtime_error("Could not open Edges.csv");}
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
    ifstream latlong("Nodes.csv"); double val2[3]; int w1, w2; string line2; 
    if(!latlong.is_open()){throw runtime_error("Could not open Nodes.csv");}
    if(latlong.good()){
    	w1 = 0;
    	while(getline(latlong, line2)){
	        stringstream ss(line2);
	        w2 = 1;
	        while(ss >> val2[0]){
				val2[w2] = val2[0];
	       		if(ss.peek() == ',') ss.ignore();
	       		w2++;
	       	}
	       	g.addLatLong(val2[1],val2[2],w1);
	       	w1++;
		}
    } latlong.close();
    return g;
}
int main(){
	Grafo rj = LeArquivo();
	while(true){
		int a; printf("Digite o no inicial: "); scanf("%d",&a);
		int b; printf("Digite o no final: "); scanf("%d",&b);
		EncontraCaminho(rj, a, b);
	}
}
