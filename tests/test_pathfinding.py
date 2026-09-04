import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from graph import GridGraph
from pathfinding import dijkstra, reconstruct_path
from world import CityMap


class DijkstraTest(unittest.TestCase):
    def setUp(self) -> None:
        self.city = CityMap(3, 3, seed=123456)
        for cell in self.city.cells:
            cell.danger = 1
        self.graph = GridGraph(self.city)

    def test_finds_a_path_and_returns_predecessors(self) -> None:
        cost, predecessors = dijkstra(self.graph, (0, 0), (2, 2))

        self.assertIsNotNone(cost)
        self.assertEqual(predecessors[(0, 0)], None)
        self.assertIn((2, 2), predecessors)

    def test_prefers_lower_danger_over_shorter_distance(self) -> None:
        self.city.cell_at(1, 0).danger = 100

        cost, predecessors = dijkstra(self.graph, (0, 0), (2, 0))

        self.assertEqual(cost, 4)
        self.assertNotEqual(predecessors[(2, 0)], (1, 0))

    def test_returns_no_cost_for_invalid_goal(self) -> None:
        cost, predecessors = dijkstra(self.graph, (0, 0), (3, 0))

        self.assertIsNone(cost)
        self.assertEqual(predecessors, {})

    def test_reconstructs_path_from_start_to_goal(self) -> None:
        cost, predecessors = dijkstra(self.graph, (0, 0), (2, 0))

        path, total_cost = reconstruct_path(
            self.graph, (0, 0), (2, 0), predecessors
        )

        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 0))
        self.assertEqual(total_cost, cost)

    def test_returns_empty_path_when_goal_has_no_predecessor(self) -> None:
        path, total_cost = reconstruct_path(
            self.graph,
            (0, 0),
            (2, 2),
            {(0, 0): None},
        )

        self.assertEqual(path, [])
        self.assertIsNone(total_cost)


if __name__ == "__main__":
    unittest.main()