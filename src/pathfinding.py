import heapq

from graph import GridGraph, Position


Predecessors = dict[Position, Position | None]


def dijkstra(
    graph: GridGraph,
    start: Position,
    goal: Position,
) -> tuple[int | None, Predecessors]:
    """Encontra o caminho de menor perigo entre dois pontos do grafo."""
    nodes = set(graph.nodes())
    if start not in nodes or goal not in nodes:
        return None, {}

    distances = {position: float("inf") for position in nodes}
    predecessors: Predecessors = {start: None}
    distances[start] = 0
    priority_queue: list[tuple[float, Position]] = [(0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance != distances[current]:
            continue
        if current == goal:
            break

        for neighbor, weight in graph.neighbors(current):
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if distances[goal] == float("inf"):
        return None, predecessors
    return int(distances[goal]), predecessors


def reconstruct_path(
    graph: GridGraph,
    start: Position,
    goal: Position,
    predecessors: Predecessors,
) -> tuple[list[Position], int | None]:
    """Reconstrói o caminho e recalcula seu custo a partir dos predecessores."""
    if start not in predecessors or goal not in predecessors:
        return [], None

    reversed_path: list[Position] = []
    current = goal
    visited: set[Position] = set()

    while current != start:
        if current in visited or current not in predecessors:
            return [], None
        visited.add(current)
        reversed_path.append(current)
        predecessor = predecessors[current]
        if predecessor is None:
            return [], None
        current = predecessor

    reversed_path.append(start)
    path = list(reversed(reversed_path))
    total_cost = sum(graph.city.cell_at(*position).danger for position in path[1:])
    return path, total_cost


def find_route_to_shelter(city: object) -> tuple[list[Position], int | None]:
    """Calcula a rota de menor perigo do humano até o abrigo."""
    shelter_position = city.position_of_place("Abrigo")
    if shelter_position is None:
        return [], None

    graph = GridGraph(city)
    start = city.player_position
    cost, predecessors = dijkstra(graph, start, shelter_position)
    if cost is None:
        return [], None
    return reconstruct_path(graph, start, shelter_position, predecessors)