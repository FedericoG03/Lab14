import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        for s in self._model.getAllStores():
            self._view._ddStore.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        numGiorni = int(self._view._txtIntK.value)
        if numGiorni == '':
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('K non valido, inserire un valore', color='red'))
            return
        try:
            intMaxG = int(numGiorni)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text('K non valido, inserire un valore', color='red'))
            return
        store = self._view._ddStore.value
        self._model.buildGraf(numGiorni,store)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {nNodes}\n"
                                                      f"Numero di archi: {nEdges}"))

        for s in self._model._grafo.nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(s))
        self._view.update_page()


    def handleCerca(self, e):
        nodeP = self._view._ddNode.value
        path = self._model.camminoLungo(nodeP)
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

    def handleRicorsione(self, e):
        nodeP = self._view._ddNode.value
        peso, percorso=self._model.getPercorsoPesoMax(nodeP)
        self._view.txt_result.controls.append(ft.Text(f"Il peso e di: {peso}"))
        self._view.txt_result.controls.append(ft.Text(f"il percorso è:"))
        for p in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.update_page()



