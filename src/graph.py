from collections.abc import Iterator


Position = tuple[int, int]
WeightedNeighbor = tuple[Position, int]


class GridGraph:
    """Representa o grid do mapa como um grafo ponderado."""

    def __init__(self, city: object):
        self.city = city

    def neighbors(self, position: Position) -> Iterator[WeightedNeighbor]:
        """Retorna vizinhos ortogonais e o perigo da célula de destino."""
        x, y = position
        if self.city.cell_at(x, y) is None:
            return

        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for offset_x, offset_y in directions:
            neighbor = self.city.cell_at(x + offset_x, y + offset_y)
            if neighbor is not None:
                yield neighbor.position, neighbor.danger

    def nodes(self) -> Iterator[Position]:
        """Retorna a posição de todas as células do mapa."""
        for cell in self.city.cells:
            yield cell.position