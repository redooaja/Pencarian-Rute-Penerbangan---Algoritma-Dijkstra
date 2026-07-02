import pandas as pd


def get_route_details(path):

    routes = pd.read_csv("data/routes.csv")

    details = []

    total_cost = 0

    for i in range(len(path) - 1):

        asal = path[i]
        tujuan = path[i + 1]

        route = routes[
            (
                (routes["asal"] == asal)
                & (routes["tujuan"] == tujuan)
            )
            |
            (
                (routes["asal"] == tujuan)
                & (routes["tujuan"] == asal)
            )
        ]

        if not route.empty:

            harga = int(route.iloc[0]["harga"])

            details.append({
                "Asal": asal,
                "Tujuan": tujuan,
                "Harga": harga
            })

            total_cost += harga

    return details, total_cost