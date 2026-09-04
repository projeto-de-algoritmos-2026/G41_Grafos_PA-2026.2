from dataclasses import dataclass
from enum import Enum
import random


class Terrain(Enum):
    ROAD = ("Rua", (88, 91, 86), 1)
    BUILDING = ("Edificio", (121, 101, 88), 4)
    PARK = ("Parque", (64, 116, 78), 2)
    RUINS = ("Ruinas", (104, 75, 73), 6)

    def __init__(self, label: str, color: tuple[int, int, int], cost: int):
        self.label = label
        self.color = color
        self.cost = cost


@dataclass(frozen=True)
class Place:
    name: str
    symbol: str
    color: tuple[int, int, int]


@dataclass
class Cell:
    x: int
    y: int
    terrain: Terrain
    place: Place | None = None

    @property
    def cost(self) -> int:
        return self.terrain.cost


PLACES = (
    Place("Hospital", "H", (238, 238, 218)),
    Place("Mercado", "M", (234, 177, 75)),
    Place("Delegacia", "D", (111, 180, 210)),
)


class CityMap:
    def __init__(self, width: int, height: int, seed: int | None = None):
        self.width = width
        self.height = height
        self.seed = seed
        self.cells: list[Cell] = []
        self.places: list[Place] = []
        self.player_position = (0, 0)
        self.generate()

    def generate(self) -> None:
        self.seed = random.randrange(100000, 999999) if self.seed is None else self.seed
        generator = random.Random(self.seed)
        self.cells = []

        for y in range(self.height):
            for x in range(self.width):
                if x % 4 == 0 or y % 4 == 0:
                    terrain = Terrain.ROAD
                else:
                    terrain = generator.choices(
                        (Terrain.BUILDING, Terrain.PARK, Terrain.RUINS),
                        weights=(52, 24, 24),
                    )[0]
                self.cells.append(Cell(x, y, terrain))

        self._place_locations(generator)
        self.player_position = (0, 0)

    def regenerate(self) -> None:
        self.seed = None
        self.generate()

    def _place_locations(self, generator: random.Random) -> None:
        self.places = list(PLACES)
        available = [cell for cell in self.cells if cell.terrain != Terrain.ROAD]
        generator.shuffle(available)

        for place, cell in zip(self.places, available):
            cell.place = place

    def cell_at(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y * self.width + x]
        return None