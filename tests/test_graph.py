import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from graph import GridGraph
from world import CityMap


class GridGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.city = CityMap(5, 5, seed=123456)
        self.graph = GridGraph(self.city)

    def test_internal_cell_has_four_neighbors(self) -> None:
        neighbors = list(self.graph.neighbors((2, 2)))

        self.assertEqual(
            {position for position, _ in neighbors},
            {(2, 1), (2, 3), (1, 2), (3, 2)},
        )

    def test_out_of_bounds_position_has_no_neighbors(self) -> None:
        self.assertEqual(list(self.graph.neighbors((-1, 0))), [])
        self.assertEqual(list(self.graph.neighbors((5, 5))), [])

    def test_edge_weight_is_destination_danger(self) -> None:
        for position, danger in self.graph.neighbors((2, 2)):
            self.assertEqual(danger, self.city.cell_at(*position).danger)


if __name__ == "__main__":
    unittest.main()