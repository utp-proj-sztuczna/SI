import json
import heapq
import math
import geopy.distance

class Graph:
#	node = []
#	nodeDistanceMatrix = []
#	indexStartNode = 0
#	indexEndtNode = 0

	def __init__(self, _node, _edge, _start, _end): # wywołanie kiedy inicjalizowany jest obiekt klasy
		self.node = [] # deklaracja pustej listy
		self.nodeDistanceMatrix = [[] for i in _node] # tworzenie pustych list zagnieżdżonych w liście self.nodeDistanceMatrix w zależności od tego ile węzłów zostało utworzonych (np. 2 węzła to 2 listy zagnieżdżone)
		for n in _node:
			self.node.append((n['lat'], n['lng'])) # pętla, która dodaje do self.node po kolei współrzędne węzłów
		for e in _edge:
			self.nodeDistanceMatrix[e['a']].append((e['b'], self.calculateDistance(e['a'], e['b'])))
			self.nodeDistanceMatrix[e['b']].append((e['a'], self.calculateDistance(e['a'], e['b']))) # zapisanie odległości między sąsiednimi punktami dla każdego węzła, 0 indeks reprezentuje pierwszy węzeł i odległości do jego sąsiadów, 1 indeks reprezentuje drugi węzeł i odległości do jego sąsiadów itd.
		self.indexStartNode = _start # zapisanie indeksu węzła początkowego
		self.indexEndtNode = _end # zapisanie indeksu węzła końcowego

	def calculateDistance(self, a, b): # metoda do obliczania dystansu między dwoma węzłami w km
		coords_1 = (self.node[a][0], self.node[a][1])
		coords_2 = (self.node[b][0], self.node[b][1]) # zapisanie w zmiennych współrzędnych obu węzłów
		return geopy.distance.vincenty(coords_1, coords_2).km # wykorzystanie biblioteki geopy do obliczenia odległości w km za pomocą formuły Vincenty

	def astar(self):
		dist = [-1 for i in self.node] # zapełnienie listy wartościami -1 w zależności od tego ile węzłów zostało utworzonych (np. 2 węzła to 2 wartości -1 w liście)
		pre  = [ i for i in range(len(self.node))] # zapełnienie listy indeksami węzłów (np. dla 4 węzłów lista będzie miała wartości 0, 1, 2, 3)
		# z pre będzie można na końcu odczytać najkrótszą ścieżkę
		# indeks listy oznacza dany węzeł, wartość pod tym indeksem oznacza indeks poprzedniego węzła, poniżej przykład:
		# mamy 5 węzłów, czyli lista będzie tak wyglądała: (0, 1, 2, 3, 4), załóżmy, że wyznaczyliśmy drogę od 1 węzła do 5 węzła
		# na końcu lista będzie wyglądała tak: (0, 1, 0, 3, 2), ze zmiennej self.indexEndNode zapisane jest, że ostatnim węzłem jest 5, czyli indeks 4 (droga: 5)
		# pod indeksem 4 w liście mamy wartość 2, czyli przed 5 węzłem będziemy przechodzili przez 3 węzeł (droga: 3-5)
		# pod indeksem 2 w liście mamy wartość 0, czyli przed 3 węzłem będziemy przechodzili przez 1 węzeł (droga: 1-3-5)
		# dotarliśmy do węzła początkowego, więc droga została wyznaczona
		pq = []
		# elementy listy pq:
		#   [0] => wartość A*
		#   [1] => aktualny dystans
		#   [2] => dest index
		#   [3] => previous vertex index
		heapq.heappush(pq, (0, 0, self.indexStartNode, self.indexStartNode)) # wstawienie do kopca pq podanych wartości
		while (len(pq) > 0): # pętla będzie działać dopóki nie natknie się na break
			top = heapq.heappop(pq) # wyciągnięcie najmniejszego elementu z kopca pq
			print(top)
			if (dist[top[2]] == -1): 
				dist[top[2]] = top[1] # zapisanie dotychczasowego dystansu, za pomocą indeksu wskazuje się na węzeł
				pre[top[2]] = top[3]
				print(pre)
				if (top[2] == self.indexEndtNode):
					break
				for n in self.nodeDistanceMatrix[top[2]]:
					heapq.heappush(pq, (top[1] + n[1] + self.calculateDistance(self.indexEndtNode, n[0]), top[1] + n[1], n[0], top[2])) 
					# zapisanie do pq wartości: 
					# (dotychczasowy dystans + dystans do następnego węzła + dystans z następnego węzła do węzła końcowego (czyli wynik algorytmu A*), dotychczasowy dystans + dystans do następnego węzła, następny węzeł, obecny węzeł)
		last = self.indexEndtNode # zapisanie do zmiennej indeksu węzła końcowego 
		route = [last] # lista, w której przechowana zostanie ścieżka do węzła końcowego oraz zapisanie indeksu węzła końcowego do tej listy
		while (last != self.indexStartNode):
			last = pre[last] # zapisanie indeksu poprzedniego węzła węzła
			route = [last] + route # dołączenie do route indeksu poprzedniego węzła 
		return {
			'route': route, # zwrócenie najkrótszej ścieżki
			'distance': dist[self.indexEndtNode] # zwrócenie dystansu
		}

def receive(req): # funkcja wywołana w index.py, do której są przesłane dane z js
	g = Graph(
		json.loads(req['node']), 
		json.loads(req['edge']),
		json.loads(req['start']),
		json.loads(req['end'])
	) # wczytanie danych z js, czyli węzłów (node), krawędzi (edge), punktu startu podróży oraz punktu końca podróży i zapisanie w obiekcie g, który pochodzi z klasy Graph
	return g.astar() # wywołanie metody astar dla obiektu g i zwrócenie jej wartości, czyli najkrótszej ścieżki i dystansu potrzebniego do jej przebycia
