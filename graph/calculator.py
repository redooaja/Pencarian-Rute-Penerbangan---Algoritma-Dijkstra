def calculate_route(graph, route):

    total_distance = 0
    total_price = 0

    for i in range(len(route) - 1):

        current = route[i]
        next_airport = route[i + 1]

        for destination in graph[current]:

            if destination[0] == next_airport:

                total_distance += destination[1]
                total_price += destination[2]

    return total_distance, total_price