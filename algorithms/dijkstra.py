import heapq

def dijkstra(graph, start, end):
    # Menyimpan biaya minimum ke setiap node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Menyimpan jalur sebelumnya
    previous = {node: None for node in graph}

    # Priority Queue
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Jika sudah sampai tujuan
        if current_node == end:
            break

        # Jika jarak sekarang lebih besar dari yang tersimpan
        if current_distance > distances[current_node]:
            continue

        for neighbor, cost in graph[current_node]:
            distance = current_distance + cost

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (distance, neighbor)
                )

    # Rekonstruksi jalur
    path = []

    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end]