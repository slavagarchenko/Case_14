
import pygame
from typing import Optional, Tuple, List
from game_logic import count_live_cells
from constants import (
    COLOR_ALIVE, COLOR_DEAD, COLOR_GRID, COLOR_FONT,
    FONT_NAME, FONT_SIZE
)
from ru_local import SYSTEM, UI

Grid = List[List[int]]


def init_display(rows: int, cols: int,
                 cell_size: int = 20) -> Tuple[pygame.Surface, int, int]:
    """
    Initialize the Pygame display window.

    Args:
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        cell_size: Size of each cell in pixels

    Returns:
        Tuple containing (screen surface, window width, window height)
    """
    width = cols * cell_size
    height = rows * cell_size

    screen: pygame.Surface = pygame.display.set_mode(
        (width, height), pygame.RESIZABLE
    )
    pygame.display.set_caption(SYSTEM["window_title"])

    return screen, width, height


def draw_ui(screen: pygame.Surface, grid: Grid, generation: int,
            speed: float, running: bool = True) -> None:
    """
    Draw the user interface overlay with game information.

    Args:
        screen: Pygame surface to draw on
        grid: Current game grid
        generation: Current generation number
        speed: Current simulation speed
        running: Whether the simulation is running or paused
    """
    pygame.font.init()
    font: pygame.font.Font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    live_cells = count_live_cells(grid)

    status = UI["running"] if running else UI["paused"]
    status_text = UI["status_format"].format(
        status,
        UI["generation"], generation,
        UI["speed"], speed,
        UI["alive"], live_cells
    )

    text_surface: pygame.Surface = font.render(
        status_text, True, COLOR_FONT
    )
    screen.blit(text_surface, (10, 10))


def draw_grid(screen: pygame.Surface, grid: Grid, generation: int,
              speed: float, cell_size: int = 20) -> None:
    """
    Draw the complete game grid with cells and grid lines.

    Args:
        screen: Pygame surface to draw on
        grid: Current game grid
        generation: Current generation number
        speed: Current simulation speed
        cell_size: Size of each cell in pixels
    """
    screen.fill(COLOR_DEAD)

    rows: int = len(grid)
    cols: int = len(grid[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                pygame.draw.rect(
                    screen,
                    COLOR_ALIVE,
                    (col * cell_size,
                     row * cell_size,
                     cell_size,
                     cell_size)
                )

    for x in range(0, cols * cell_size, cell_size):
        pygame.draw.line(
            screen,
            COLOR_GRID,
            (x, 0),
            (x, rows * cell_size)
        )

    for y in range(0, rows * cell_size, cell_size):
        pygame.draw.line(
            screen,
            COLOR_GRID,
            (0, y),
            (cols * cell_size, y)
        )

    draw_ui(screen, grid, generation, speed)

    pygame.display.update()


def get_cell_from_mouse(pos: Tuple[int, int], cell_size: int
                        ) -> Optional[Tuple[int, int]]:
    """
    Convert mouse screen coordinates to grid cell coordinates.

    Args:
        pos: Mouse position as (x, y) tuple
        cell_size: Size of each cell in pixels

    Returns:
        Tuple of (row, col) if within grid bounds, None otherwise
    """
    x: int
    y: int
    x, y = pos

    if x < 0 or y < 0:
        return None

    row: int = y // cell_size
    col: int = x // cell_size

    return row, col
