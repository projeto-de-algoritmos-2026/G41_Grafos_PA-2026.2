import sys

import pygame

from world import CityMap, Terrain


TITLE = "Rota do Abrigo"
WINDOW_WIDTH = 1120
WINDOW_HEIGHT = 640
TILE_SIZE = 32
MAP_WIDTH = 25
MAP_HEIGHT = 17
SIDEBAR_WIDTH = WINDOW_WIDTH - MAP_WIDTH * TILE_SIZE


COLORS = {
    "background": (18, 22, 27),
    "panel": (30, 36, 43),
    "text": (232, 236, 228),
    "muted": (157, 166, 165),
    "grid": (45, 52, 57),
}


def draw_place_icon(screen: pygame.Surface, place: object, rectangle: pygame.Rect) -> None:
    x, y = rectangle.x + 4, rectangle.y + 3
    outline = (45, 38, 39)
    place_name = place.name
    body = pygame.Rect(x + 3, y + 10, 22, 15)
    pygame.draw.rect(screen, outline, body.inflate(3, 3), border_radius=3)

    if place_name == "Abrigo":
        pygame.draw.polygon(screen, outline, [(x + 1, y + 12), (x + 14, y + 2), (x + 27, y + 12)])
        pygame.draw.polygon(screen, (224, 92, 76), [(x + 4, y + 11), (x + 14, y + 4), (x + 24, y + 11)])
        pygame.draw.rect(screen, (214, 159, 80), body, border_radius=2)
        pygame.draw.rect(screen, (93, 62, 55), (x + 11, y + 17, 6, 8), border_radius=1)
        pygame.draw.circle(screen, (245, 190, 92), (x + 16, y + 21), 1)
    elif place_name == "Hospital":
        pygame.draw.rect(screen, (238, 238, 218), body, border_radius=2)
        pygame.draw.polygon(screen, outline, [(x + 1, y + 11), (x + 14, y + 3), (x + 27, y + 11)])
        pygame.draw.polygon(screen, (224, 92, 76), [(x + 4, y + 10), (x + 14, y + 5), (x + 24, y + 10)])
        pygame.draw.rect(screen, (224, 92, 76), (x + 11, y + 6, 6, 10))
        pygame.draw.rect(screen, (224, 92, 76), (x + 9, y + 8, 10, 6))
    elif place_name == "Mercado":
        pygame.draw.rect(screen, (234, 177, 75), body, border_radius=2)
        pygame.draw.rect(screen, (245, 225, 152), (x + 3, y + 11, 22, 5))
        for stripe_x in (x + 5, x + 13, x + 21):
            pygame.draw.rect(screen, (190, 73, 52), (stripe_x, y + 11, 4, 5))
        pygame.draw.rect(screen, (94, 65, 52), (x + 11, y + 18, 6, 7))
        pygame.draw.rect(screen, (72, 105, 94), (x + 5, y + 18, 4, 4))
    else:
        pygame.draw.rect(screen, (111, 180, 210), body, border_radius=2)
        pygame.draw.polygon(screen, outline, [(x + 1, y + 11), (x + 14, y + 3), (x + 27, y + 11)])
        pygame.draw.polygon(screen, (48, 78, 104), [(x + 4, y + 10), (x + 14, y + 5), (x + 24, y + 10)])
        pygame.draw.rect(screen, (207, 224, 228), (x + 11, y + 17, 6, 8))
        pygame.draw.circle(screen, (245, 193, 76), (x + 14, y + 14), 3)
        pygame.draw.line(screen, (48, 78, 104), (x + 12, y + 14), (x + 16, y + 14), 1)


def draw_terrain_art(screen: pygame.Surface, cell: object, rectangle: pygame.Rect) -> None:
    x, y = rectangle.x + 4, rectangle.y + 3
    outline = (45, 38, 39)
    ground = rectangle.bottom - 4

    if cell.terrain.name == "PARK":
        pygame.draw.ellipse(screen, (35, 82, 52), (x + 1, y + 14, 11, 12))
        pygame.draw.ellipse(screen, (46, 105, 62), (x + 4, y + 7, 12, 13))
        pygame.draw.ellipse(screen, (35, 82, 52), (x + 12, y + 12, 13, 13))
        pygame.draw.rect(screen, (105, 70, 46), (x + 8, y + 17, 3, 10))
        pygame.draw.rect(screen, (105, 70, 46), (x + 18, y + 18, 3, 9))
        pygame.draw.rect(screen, (190, 139, 76), (x + 13, y + 22, 10, 3), border_radius=1)
    elif cell.terrain.name == "BUILDING":
        body = pygame.Rect(x + 3, y + 10, 22, 15)
        pygame.draw.rect(screen, outline, body.inflate(3, 3), border_radius=3)
        pygame.draw.rect(screen, (164, 134, 108), body, border_radius=2)
        pygame.draw.polygon(screen, (207, 173, 111), [(x + 1, y + 11), (x + 14, y + 3), (x + 27, y + 11)])
        for window_x in (x + 6, x + 18):
            pygame.draw.rect(screen, (55, 82, 88), (window_x, y + 14, 5, 5), border_radius=1)
        pygame.draw.rect(screen, (75, 52, 48), (x + 11, y + 19, 6, 6), border_radius=1)
    elif cell.terrain.name == "RUINS":
        pygame.draw.polygon(screen, outline, [(x + 2, ground), (x + 3, y + 12), (x + 9, y + 15), (x + 13, y + 7), (x + 18, y + 13), (x + 24, y + 10), (x + 26, ground)])
        pygame.draw.polygon(screen, (145, 102, 91), [(x + 4, ground - 2), (x + 5, y + 13), (x + 9, y + 16), (x + 13, y + 9), (x + 17, y + 15), (x + 23, y + 12), (x + 24, ground - 2)])
        pygame.draw.circle(screen, (190, 136, 91), (x + 7, ground - 2), 2)
        pygame.draw.circle(screen, (190, 136, 91), (x + 20, ground - 1), 2)


def draw_cartoon_icon(screen: pygame.Surface, cell: object, rectangle: pygame.Rect) -> None:
    if getattr(cell, "place", None):
        draw_place_icon(screen, cell.place, rectangle)
    else:
        draw_terrain_art(screen, cell, rectangle)


def draw_player(screen: pygame.Surface, center: tuple[int, int]) -> None:
    x, y = center
    outline = (45, 38, 39)
    pygame.draw.circle(screen, outline, (x, y - 8), 5)
    pygame.draw.circle(screen, (235, 177, 125), (x, y - 8), 3)
    pygame.draw.polygon(screen, outline, [(x - 7, y - 2), (x + 7, y - 2), (x + 5, y + 8), (x - 5, y + 8)])
    pygame.draw.polygon(screen, (239, 193, 76), [(x - 5, y - 1), (x + 5, y - 1), (x + 4, y + 6), (x - 4, y + 6)])
    pygame.draw.line(screen, outline, (x - 5, y), (x - 9, y + 5), 2)
    pygame.draw.line(screen, outline, (x + 5, y), (x + 9, y + 5), 2)
    pygame.draw.line(screen, outline, (x - 3, y + 7), (x - 5, y + 12), 2)
    pygame.draw.line(screen, outline, (x + 3, y + 7), (x + 5, y + 12), 2)


def draw_zombie(screen: pygame.Surface, center: tuple[int, int]) -> None:
    x, y = center
    outline = (45, 38, 39)
    skin = (139, 184, 126)
    pygame.draw.circle(screen, outline, (x, y - 7), 6)
    pygame.draw.circle(screen, skin, (x, y - 7), 4)
    pygame.draw.circle(screen, outline, (x - 2, y - 8), 1)
    pygame.draw.circle(screen, outline, (x + 2, y - 8), 1)
    pygame.draw.polygon(screen, outline, [(x - 7, y - 1), (x + 7, y - 1), (x + 5, y + 8), (x - 5, y + 8)])
    pygame.draw.polygon(screen, (105, 61, 71), [(x - 5, y), (x + 5, y), (x + 4, y + 6), (x - 4, y + 6)])
    pygame.draw.line(screen, outline, (x - 5, y), (x - 10, y + 4), 2)
    pygame.draw.line(screen, outline, (x + 5, y), (x + 10, y + 4), 2)
    pygame.draw.line(screen, outline, (x - 3, y + 7), (x - 5, y + 12), 2)
    pygame.draw.line(screen, outline, (x + 3, y + 7), (x + 5, y + 12), 2)


def draw_map(screen: pygame.Surface, city: CityMap, font: pygame.font.Font) -> None:
    for cell in city.cells:
        rectangle = pygame.Rect(cell.x * TILE_SIZE, cell.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, cell.terrain.color, rectangle)
        pygame.draw.rect(screen, COLORS["grid"], rectangle, 1)

        draw_cartoon_icon(screen, cell, rectangle)

    for zombie in city.zombies:
        zombie_center = (zombie.x * TILE_SIZE + TILE_SIZE // 2, zombie.y * TILE_SIZE + TILE_SIZE // 2)
        draw_zombie(screen, zombie_center)

    player = city.player_position
    player_center = (player[0] * TILE_SIZE + TILE_SIZE // 2, player[1] * TILE_SIZE + TILE_SIZE // 2)
    draw_player(screen, player_center)

def draw_sidebar(screen: pygame.Surface, city: CityMap, title_font: pygame.font.Font, font: pygame.font.Font) -> None:
    left = MAP_WIDTH * TILE_SIZE
    pygame.draw.rect(screen, COLORS["panel"], (left, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, COLORS["grid"], (left, 0), (left, WINDOW_HEIGHT), 2)

    screen.blit(title_font.render(TITLE, True, COLORS["text"]), (left + 22, 26))
    screen.blit(font.render("Uma cidade. Uma rota. Pouco tempo.", True, COLORS["muted"]), (left + 22, 66))

    y = 122
    screen.blit(font.render(f"Semente: {city.seed}", True, COLORS["text"]), (left + 22, y))
    screen.blit(font.render("R  gerar nova cidade", True, COLORS["muted"]), (left + 22, y + 28))
    screen.blit(font.render("ESC  sair", True, COLORS["muted"]), (left + 22, y + 52))

    y += 96
    screen.blit(title_font.render("Personagens", True, COLORS["text"]), (left + 22, y))
    draw_player(screen, (left + 30, y + 35))
    screen.blit(font.render("Sobrevivente", True, COLORS["text"]), (left + 54, y + 27))
    draw_zombie(screen, (left + 30, y + 68))
    screen.blit(font.render("Zumbi", True, COLORS["text"]), (left + 54, y + 60))

    y += 100
    screen.blit(title_font.render("Locais", True, COLORS["text"]), (left + 22, y))
    for place in city.places:
        y += 38
        draw_place_icon(screen, place, pygame.Rect(left + 14, y - 3, 32, 32))
        screen.blit(font.render(place.name, True, COLORS["text"]), (left + 52, y + 5))

    y += 42
    screen.blit(title_font.render("Terrenos", True, COLORS["text"]), (left + 22, y))
    for terrain in Terrain:
        y += 38
        terrain_rectangle = pygame.Rect(left + 14, y - 3, 32, 32)
        pygame.draw.rect(screen, terrain.color, terrain_rectangle)
        draw_terrain_art(screen, type("LegendCell", (), {"terrain": terrain})(), terrain_rectangle)
        screen.blit(font.render(terrain.label, True, COLORS["muted"]), (left + 52, y + 5))


def main() -> None:
    global TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH

    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    TILE_SIZE = min(42, WINDOW_WIDTH // (MAP_WIDTH + 8), WINDOW_HEIGHT // MAP_HEIGHT)
    SIDEBAR_WIDTH = WINDOW_WIDTH - MAP_WIDTH * TILE_SIZE
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 30)
    font = pygame.font.Font(None, 21)
    city = CityMap(MAP_WIDTH, MAP_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    city.regenerate()

        screen.fill(COLORS["background"])
        draw_map(screen, city, font)
        draw_sidebar(screen, city, title_font, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()