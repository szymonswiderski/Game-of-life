import pygame
import random

# --- USTAWIENIA GŁÓWNE ---
WIDTH, HEIGHT = 800, 650
MENU_HEIGHT = 120
CELL_SIZE = 10

ROWS = (HEIGHT - MENU_HEIGHT) // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# --- INICJALIZACJA PYGAME ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gra w Życie - Symulator")
try:
    font = pygame.font.SysFont("Arial", 14, bold=True)
except:
    font = pygame.font.Font(None, 18)

clock = pygame.time.Clock()

# Kolory - Podstawowe
BG_COLOR = (20, 20, 20)
GRID_COLOR = (30, 30, 30)
ALIVE_COLOR_STD = (0, 255, 200)
DEAD_COLOR = (20, 20, 20)

# Kolory - Interfejs
BTN_COLOR = (60, 60, 60)
BTN_HOVER_COLOR = (90, 90, 90)
TEXT_COLOR = (255, 255, 255)
INFO_COLOR = (200, 200, 50)
DISCO_COLOR = (180, 0, 255)
HINT_COLOR = (255, 180, 50)


# --- FUNKCJE LOGIKI GRY ---
def create_empty_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def update_grid(grid):
    new_grid = create_empty_grid()
    for y in range(ROWS):
        for x in range(COLS):
            alive_neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = (y + dy) % ROWS, (x + dx) % COLS
                    alive_neighbors += grid[ny][nx]

            if grid[y][x] == 1:
                if alive_neighbors in [2, 3]:
                    new_grid[y][x] = 1
            else:
                if alive_neighbors == 3:
                    new_grid[y][x] = 1
    return new_grid


def get_disco_color(x, y, generation):
    t = generation * 10
    r = int((x * 4 + t) % 256)
    g = int((y * 4 + t * 0.5) % 256)
    b = int(((x + y) * 2 + t * 1.5) % 256)
    return (max(70, r), max(70, g), max(70, b))


def draw_grid_and_cells(surface, grid, generation, disco_mode):
    surface.fill(BG_COLOR)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 1:
                if disco_mode:
                    color = get_disco_color(x, y, generation)
                else:
                    color = ALIVE_COLOR_STD

                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, color, rect)

            grid_rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, grid_rect, 1)


def draw_menu(surface, buttons, mouse_pos, generation, fps, disco_mode):
    surface.fill((25, 25, 25), (0, HEIGHT - MENU_HEIGHT, WIDTH, MENU_HEIGHT))
    pygame.draw.line(surface, TEXT_COLOR, (0, HEIGHT - MENU_HEIGHT), (WIDTH, HEIGHT - MENU_HEIGHT), 2)

    for name, rect in buttons.items():
        if name == "DYSKOTEKA" and disco_mode:
            curr_btn_color = DISCO_COLOR
            pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=5)
        else:
            curr_btn_color = BTN_HOVER_COLOR if rect.collidepoint(mouse_pos) else BTN_COLOR

        pygame.draw.rect(surface, curr_btn_color, rect, border_radius=5)
        pygame.draw.rect(surface, TEXT_COLOR, rect, 2, border_radius=5)

        text_surface = font.render(name, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    # --- TEKSTY I STATYSTYKI PO PRAWEJ STRONIE ---
    # Ustawiamy sztywną pozycję tekstu za ostatnim przyciskiem (X = 645)
    text_x = 645

    # Statystyki (żółte)
    surface.blit(font.render(f"POKOLENIE: {generation}", True, INFO_COLOR), (text_x, HEIGHT - 105))
    surface.blit(font.render(f"PRĘDKOŚĆ: {fps} FPS", True, INFO_COLOR), (text_x, HEIGHT - 85))

    # Instrukcje w dwóch linijkach (pomarańczowe)
    surface.blit(font.render("MYSZKA: rysowanie", True, HINT_COLOR), (text_x, HEIGHT - 55))
    surface.blit(font.render("STRZAŁKI: prędkość", True, HINT_COLOR), (text_x, HEIGHT - 35))


# --- GOTOWE STRUKTURY (PRESETS) ---
def insert_preset(grid, coords, center=False):
    offset_y = ROWS // 2 if center else 0
    offset_x = COLS // 2 if center else 0
    for dy, dx in coords:
        y, x = (offset_y + dy) % ROWS, (offset_x + dx) % COLS
        grid[y][x] = 1


def insert_glider(grid):
    coords = [[0, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    insert_preset(grid, coords)


def insert_gosper_gun(grid):
    gun = [[5, 1], [5, 2], [6, 1], [6, 2], [5, 11], [6, 11], [7, 11], [4, 12],
           [8, 12], [3, 13], [9, 13], [3, 14], [9, 14], [6, 15], [4, 16], [8, 16],
           [5, 17], [6, 17], [7, 17], [6, 18], [3, 21], [4, 21], [5, 21], [3, 22],
           [4, 22], [5, 22], [2, 23], [6, 23], [1, 25], [2, 25], [6, 25], [7, 25],
           [3, 35], [4, 35], [3, 36], [4, 36]]
    insert_preset(grid, gun)


def insert_r_pentomino(grid):
    coords = [[0, 1], [0, 2], [1, 0], [1, 1], [2, 1]]
    insert_preset(grid, coords, center=True)


def insert_lwss(grid):
    coords = [[0, 1], [0, 4], [1, 0], [2, 0], [2, 4], [3, 0], [3, 1], [3, 2], [3, 3]]
    insert_preset(grid, coords, center=True)


def insert_pulsar(grid):
    pulsar = []
    for dy in [-6, -1, 1, 6]:
        for dx in [-4, -3, -2, 2, 3, 4]: pulsar.append([dy, dx])
    for dy in [-4, -3, -2, 2, 3, 4]:
        for dx in [-6, -1, 1, 6]: pulsar.append([dy, dx])
    insert_preset(grid, pulsar, center=True)


# --- GŁÓWNA PĘTLA PROGRAMU ---
def main():
    grid = create_empty_grid()
    running = True
    playing = False

    generation = 0
    fps_speed = 15
    disco_mode = False
    drawing = False

    btn_w1 = 140;
    btn_w2 = 90
    gap = 10;
    start_x = 20
    btn_y1 = HEIGHT - 105
    btn_y2 = HEIGHT - 55

    buttons = {
        "START / PAUZA": pygame.Rect(start_x, btn_y1, btn_w1, 40),
        "LOSUJ": pygame.Rect(start_x + btn_w1 + gap, btn_y1, btn_w2, 40),
        "WYCZYŚĆ": pygame.Rect(start_x + btn_w1 + gap + btn_w2 + gap, btn_y1, btn_w2, 40),

        "GLIDER": pygame.Rect(start_x, btn_y2, btn_w2, 40),
        "DZIAŁO": pygame.Rect(start_x + btn_w2 + gap, btn_y2, btn_w2, 40),
        "R-PENT": pygame.Rect(start_x + (btn_w2 + gap) * 2, btn_y2, btn_w2, 40),
        "STATEK": pygame.Rect(start_x + (btn_w2 + gap) * 3, btn_y2, btn_w2, 40),
        "PULSAR": pygame.Rect(start_x + (btn_w2 + gap) * 4, btn_y2, btn_w2, 40),
        "DYSKOTEKA": pygame.Rect(start_x + (btn_w2 + gap) * 5, btn_y2, 110, 40)
    }

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fps_speed = min(60, fps_speed + 5)
                elif event.key == pygame.K_DOWN:
                    fps_speed = max(1, fps_speed - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mouse_pos[1] < HEIGHT - MENU_HEIGHT:
                        drawing = True
                        x = mouse_pos[0] // CELL_SIZE
                        y = mouse_pos[1] // CELL_SIZE
                        grid[y][x] = 1 if grid[y][x] == 0 else 0
                    else:
                        if buttons["START / PAUZA"].collidepoint(mouse_pos):
                            playing = not playing
                        elif buttons["LOSUJ"].collidepoint(mouse_pos):
                            grid = [[random.choice([0, 1]) if random.random() < 0.2 else 0 for _ in range(COLS)] for _
                                    in range(ROWS)]
                            generation = 0
                        elif buttons["WYCZYŚĆ"].collidepoint(mouse_pos):
                            grid = create_empty_grid()
                            playing = False
                            generation = 0
                        elif buttons["GLIDER"].collidepoint(mouse_pos):
                            insert_glider(grid)
                        elif buttons["DZIAŁO"].collidepoint(mouse_pos):
                            insert_gosper_gun(grid)
                        elif buttons["R-PENT"].collidepoint(mouse_pos):
                            insert_r_pentomino(grid)
                        elif buttons["STATEK"].collidepoint(mouse_pos):
                            insert_lwss(grid)
                        elif buttons["PULSAR"].collidepoint(mouse_pos):
                            insert_pulsar(grid)
                        elif buttons["DYSKOTEKA"].collidepoint(mouse_pos):
                            disco_mode = not disco_mode

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: drawing = False

            elif event.type == pygame.MOUSEMOTION and drawing:
                if mouse_pos[1] < HEIGHT - MENU_HEIGHT:
                    x = mouse_pos[0] // CELL_SIZE
                    y = mouse_pos[1] // CELL_SIZE
                    if 0 <= y < ROWS and 0 <= x < COLS: grid[y][x] = 1

        if playing:
            grid = update_grid(grid)
            generation += 1

        draw_grid_and_cells(screen, grid, generation, disco_mode)
        draw_menu(screen, buttons, mouse_pos, generation, fps_speed, disco_mode)

        pygame.display.flip()
        clock.tick(fps_speed)

    pygame.quit()


if __name__ == "__main__":
    main()
