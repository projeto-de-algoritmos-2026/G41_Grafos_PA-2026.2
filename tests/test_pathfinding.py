import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from graph import GridGraph
from pathfinding import dijkstra, find_route_to_shelter, reconstruct_path
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

    def test_finds_route_from_human_to_shelter(self) -> None:
        path, total_cost = find_route_to_shelter(self.city)
        shelter_position = self.city.position_of_place("Abrigo")

        self.assertEqual(path[0], self.city.player_position)
        self.assertEqual(path[-1], shelter_position)
        expected_cost = sum(
            self.city.cell_at(*position).danger for position in path[1:]
        )
        self.assertEqual(total_cost, expected_cost)

    def test_shelter_exists_for_multiple_seeds(self) -> None:
        routes = []
        for seed in range(10):
            city = CityMap(5, 5, seed=seed)
            path, total_cost = find_route_to_shelter(city)

            self.assertIsNotNone(city.position_of_place("Abrigo"))
            self.assertTrue(path)
            self.assertIsNotNone(total_cost)
            routes.append(tuple(path))

        self.assertGreater(len(set(routes)), 1)


if __name__ == "__main__":
    unittest.main()