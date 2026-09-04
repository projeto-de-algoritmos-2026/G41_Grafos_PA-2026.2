from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import random


class Terrain(Enum):
    ROAD = ("Rua", (88, 91, 86), 1, 5)
    BUILDING = ("Edificio", (121, 101, 88), 4, 25)
    PARK = ("Parque", (64, 116, 78), 2, 10)
    RUINS = ("Ruinas", (104, 75, 73), 6, 60)

    def __init__(self, label: str, color: tuple[int, int, int], cost: int, base_danger: int):
        self.label = label
        self.color = color
        self.cost = cost
        self.base_danger = base_danger


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
    danger: int = 0

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def cost(self) -> int:
        return self.terrain.cost


@dataclass(frozen=True)
class Zombie:
    x: int
    y: int

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y


PLACES = (
    Place("Abrigo", "A", (224, 92, 76)),
    Place("Hospital", "H", (238, 238, 218)),
    Place("Mercado", "M", (234, 177, 75)),
    Place("Delegacia", "D", (111, 180, 210)),
)
ZOMBIE_COUNT = 8


class CityMap:
    def __init__(self, width: int, height: int, seed: int | None = None):
        self.width = width
        self.height = height
        self.seed = seed
        self.cells: list[Cell] = []
        self.places: list[Place] = []
        self.player_position = (0, 0)
        self.zombies: list[Zombie] = []
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
        self._spawn_zombies(generator)
        self._calculate_danger()

    def regenerate(self) -> None:
        self.seed = None
        self.generate()

    def _place_locations(self, generator: random.Random) -> None:
        self.places = list(PLACES)
        available = [cell for cell in self.cells if cell.terrain != Terrain.ROAD]
        generator.shuffle(available)

        for place, cell in zip(self.places, available):
            cell.place = place

    def _spawn_zombies(self, generator: random.Random) -> None:
        occupied = {self.player_position}
        occupied.update((cell.x, cell.y) for cell in self.cells if cell.place)
        available = [
            cell
            for cell in self.cells
            if cell.terrain == Terrain.ROAD and (cell.x, cell.y) not in occupied
        ]
        generator.shuffle(available)
        self.zombies = [Zombie(cell.x, cell.y) for cell in available[:ZOMBIE_COUNT]]

    def _calculate_danger(self) -> None:
        for cell in self.cells:
            danger = cell.terrain.base_danger
            for zombie in self.zombies:
                distance = abs(cell.x - zombie.x) + abs(cell.y - zombie.y)
                if distance == 0:
                    danger += 45
                elif distance <= 3:
                    danger += 15 // distance
            cell.danger = min(100, danger)

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "player_position": list(self.player_position),
            "cells": [
                {
                    "position": list(cell.position),
                    "terrain": cell.terrain.name,
                    "danger": cell.danger,
                    "place": cell.place.name if cell.place else None,
                }
                for cell in self.cells
            ],
            "zombies": [list(zombie.position) for zombie in self.zombies],
        }

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def from_dict(cls, data: dict) -> "CityMap":
        city = cls.__new__(cls)
        city.width = data["width"]
        city.height = data["height"]
        city.seed = data["seed"]
        place_by_name = {place.name: place for place in PLACES}
        city.cells = []
        for item in data["cells"]:
            x, y = item["position"]
            place = place_by_name.get(item["place"])
            city.cells.append(Cell(x, y, Terrain[item["terrain"]], place, item["danger"]))
        city.places = [cell.place for cell in city.cells if cell.place]
        city.player_position = tuple(data["player_position"])
        city.zombies = [Zombie(x, y) for x, y in data["zombies"]]
        return city

    @classmethod
    def load(cls, path: str | Path) -> "CityMap":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def cell_at(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y * self.width + x]
        return None