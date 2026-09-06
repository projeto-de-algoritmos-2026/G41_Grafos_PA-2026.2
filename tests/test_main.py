import os
import sys
import unittest
from pathlib import Path


os.environ["SDL_VIDEODRIVER"] = "dummy"
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import pygame

from main import COLORS, advance_player, draw_path
from pathfinding import find_route_to_shelter
from world import CityMap


class DrawPathTest(unittest.TestCase):
    def setUp(self) -> None:
        pygame.init()
        self.screen = pygame.Surface((160, 160))
        self.screen.fill((0, 0, 0))

    def tearDown(self) -> None:
        pygame.quit()

    def test_route_is_drawn_at_start_and_end_cells(self) -> None:
        draw_path(self.screen, [(0, 0), (1, 0), (2, 0)])

        route_color = COLORS["route"]
        self.assertEqual(self.screen.get_at((16, 16))[:3], route_color)
        self.assertEqual(self.screen.get_at((80, 16))[:3], route_color)

    def test_empty_route_does_not_draw(self) -> None:
        draw_path(self.screen, [])

        self.assertEqual(self.screen.get_at((16, 16))[:3], (0, 0, 0))


class PlayerMovementTest(unittest.TestCase):
    def test_player_follows_every_route_point_until_shelter(self) -> None:
        city = CityMap(5, 5, seed=7)
        path, _ = find_route_to_shelter(city)
        path_index = 0

        for expected_position in path[1:]:
            path_index = advance_player(city, path, path_index)
            self.assertEqual(city.player_position, expected_position)

        self.assertEqual(city.player_position, path[-1])
        final_index = advance_player(city, path, path_index)
        self.assertEqual(final_index, path_index)
        self.assertEqual(city.player_position, path[-1])


if __name__ == "__main__":
    unittest.main()