import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._bestPath = []
        self._bestPeso = 0
        self._idMap = {}

    def getAllStores(self):
        return DAO.getAllStores()

    def buildGraf(self, numGiorni, store):
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAllNodes(store))
        for o in DAO.getAllNodes(store):
            self._idMap[o.order_id] = o
        for edge in DAO.getAllEdges(numGiorni, store, self._idMap):
            self._grafo.add_edge(edge[0], edge[1], weight=edge[2])

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def camminoLungo(self, start_node):
        source = self._idMap[int(start_node)]
        lp = []

        # for source in self._graph.nodes:
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp

    def getPercorsoPesoMax(self,nodeP):
        self._bestPath=[]
        self._bestPeso=0

        parziale = [self._idMap[int(nodeP)]]
        self._ricosione(parziale)
        return self._bestPeso, self._bestPath


    def _ricosione(self,parziale):
        if len(parziale)>1:
            if self._bestPeso < self.calcolaPeso(parziale):
                self._bestPeso = self.calcolaPeso(parziale)
                self._bestPath = copy.deepcopy(parziale)
            for n in self._grafo.neighbors(parziale[-1]):
                if n not in parziale:
                    if self._grafo[parziale[-2]][parziale[-1]]['weight'] > self._grafo[parziale[-1]][n]['weight']:
                        parziale.append(n)
                        self._ricosione(parziale)
                        parziale.pop()
        else:
            for n in self._grafo.neighbors(parziale[-1]):
                parziale.append(n)
                self._ricosione(parziale)
                parziale.pop()

    def calcolaPeso(self, parziale):
        peso = 0
        for p in range(len(parziale)-1):
            if self._grafo.has_edge(parziale[p], parziale[p + 1]):
                peso += self._grafo[parziale[p]][parziale[p + 1]]['weight']
        return peso




