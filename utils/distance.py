from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2


def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


def calculate_total_distance(
    path,
    airports
):

    total_distance = 0

    for i in range(len(path) - 1):

        a = airports[
            airports["kode"] == path[i]
        ].iloc[0]

        b = airports[
            airports["kode"] == path[i + 1]
        ].iloc[0]

        total_distance += haversine(
            a["lat"],
            a["lon"],
            b["lat"],
            b["lon"]
        )

    return round(total_distance)