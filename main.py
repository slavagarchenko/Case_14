import pygame
from typing import List, Tuple

from display import init_display, draw_grid, get_cell_from_mouse
from game_logic import next_generation, copy_grid
from grid_io import random_grid, set_cell, reading_grid, writing_grid
from constants import (
    ROWS, COLS, CELL_SIZE, FPS, MIN_SPEED, MAX_SPEED,
    SPEED_STEP, FILENAME, RANDOM_PROB
)
from ru_local import SYSTEM, SIMULATION, FILES


Grid = List[List[int]]


def handle_events(grid: Grid, running_flag: bool, speed: int, generation: int,
                  initial_grid: Grid) -> Tuple[Grid, bool, int, int]:
    """
    Handle all pygame events and update game state accordingly.

    Args:
        grid: Current game grid
        running_flag: Whether the simulation is running
        speed: Current simulation speed (FPS)
        generation: Current generation number
        initial_grid: Initial grid state for reset functionality

    Returns:
        Tuple containing (updated grid, updated running flag, updated speed, 
            updated generation)
    """
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running_flag = False

            case pygame.MOUSEBUTTONDOWN:
                cell_pos = get_cell_from_mouse(event.pos, CELL_SIZE)
                if cell_pos:
                    row, col = cell_pos
                    set_cell(grid, row, col, 1 - grid[row][col])

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        speed = 0 if speed > 0 else FPS

                    case pygame.K_r:
                        grid = copy_grid(initial_grid)
                        generation = 0
                        print(SIMULATION["msg_reset"])

                    case pygame.K_s:
                        grid = random_grid(ROWS, COLS, prob=RANDOM_PROB)
                        initial_grid[:] = copy_grid(grid)
                        generation = 0
                        print(SIMULATION["msg_random"])

                    case pygame.K_l:
                        grid = reading_grid(FILENAME, ROWS, COLS)
                        initial_grid[:] = copy_grid(grid)
                        generation = 0
                        print(FILES["file_loaded"].format(FILENAME))

                    case pygame.K_f:
                        writing_grid(grid, FILENAME)
                        print(FILES["file_saved"].format(FILENAME))

                    case pygame.K_PLUS | pygame.K_EQUALS:
                        speed = min(speed + SPEED_STEP, MAX_SPEED)
                        print(SIMULATION["msg_speed_changed"].format(speed))

                    case pygame.K_MINUS:
                        speed = max(speed - SPEED_STEP, MIN_SPEED)
                        print(SIMULATION["msg_speed_changed"].format(speed))

                    case pygame.K_q:
                        running_flag = False

    return grid, running_flag, speed, generation


def main() -> None:
    """
    Main game loop for Conway's Game of Life.
    Initializes the display, handles events, updates generations, and renders the grid.
    """
    grid = random_grid(ROWS, COLS, prob=RANDOM_PROB)
    initial_grid = copy_grid(grid)
    generation = 0
    speed = FPS
    running_flag = True

    screen, width, height = init_display(ROWS, COLS, CELL_SIZE)
    clock = pygame.time.Clock()
    last_update = pygame.time.get_ticks()

    print(SYSTEM["running_full_simulation"])
    print(SYSTEM["generation_info"].format(generation))
    print(SYSTEM["live_cells_info"].format(sum(sum(row) for row in grid)))

    while running_flag:
        grid, running_flag, speed, generation = handle_events(
            grid, running_flag, speed, generation, initial_grid
        )

        if speed > 0:
            now = pygame.time.get_ticks()
            delay = 1000 / speed
            if now - last_update >= delay:
                grid = next_generation(grid)
                generation += 1
                last_update = now

        draw_grid(screen, grid, generation, speed, cell_size=CELL_SIZE)

        clock.tick(FPS)

    pygame.quit()
    print(SYSTEM["simulation_end"])


if __name__ == "__main__":
    main()
