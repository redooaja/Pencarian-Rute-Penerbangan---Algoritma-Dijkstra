import pandas as pd

def load_graph():
    routes = pd.read_csv("data/routes.csv")

    graph = {}

    for _, row in routes.iterrows():

        asal = row["asal"]
        tujuan = row["tujuan"]
        harga = row["harga"]

        if asal not in graph:
            graph[asal] = []

        if tujuan not in graph:
            graph[tujuan] = []

        #Fungsi untuk membuat graph searah menjadi 2 arah!!!!!!!
        graph[asal].append((tujuan, harga))
        graph[tujuan].append((asal, harga))

    return graph