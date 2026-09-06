import os
import sys
import unittest
from pathlib import Path


os.environ["SDL_VIDEODRIVER"] = "dummy"
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import pygame

from main import COLORS, draw_path


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


if __name__ == "__main__":
    unittest.main()