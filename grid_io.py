import random
from typing import List, Tuple
from constants import RANDOM_PROB
from ru_local import FILES, ERRORS


Grid = List[List[int]]
Coordinates = List[Tuple[int, int]]

PRESET_PATTERNS: dict[str, Coordinates] = {
    'block': [(0, 0), (0, 1), (1, 0), (1, 1)]
}


def create_empty_grid(rows: int, columns: int) -> Grid:
    """
    Create a grid filled with zeros.

    Args:
        rows: Number of rows
        columns: Number of columns

    Returns:
        2D list representing empty grid
    """
    return [[0] * columns for _ in range(rows)]


def random_grid(rows: int, columns: int, prob: float = RANDOM_PROB) -> Grid:
    """
    Generate a random grid where each cell has probability 
        'prob' of being alive.

    Args:
        rows: Number of rows
        columns: Number of columns
        prob: Probability of a cell being alive (0.0 to 1.0)

    Returns:
        2D list with random live cells
    """
    grid: Grid = create_empty_grid(rows, columns)
    for row in range(rows):
        for col in range(columns):
            if random.random() < prob:
                grid[row][col] = 1
            else:
                grid[row][col] = 0
    return grid


def reading_grid(filename: str, rows: int, columns: int) -> Grid:
    """
    Read grid configuration from a file.
    File format: each line contains "row col" coordinates of live cells.

    Args:
        filename: Path to the input file
        rows: Number of rows in the grid
        columns: Number of columns in the grid

    Returns:
        2D list with live cells set according to file content
    """
    grid: Grid = create_empty_grid(rows, columns)
    try:
        with open(filename, 'r') as f:
            for line in f:
                line: str = line.strip()
                if not line:
                    continue
                parts: List[str] = line.split()
                if len(parts) == 2:
                    r: int = int(parts[0])
                    c: int = int(parts[1])
                    if 0 <= r < rows and 0 <= c < columns:
                        grid[r][c] = 1
                    else:
                        print(FILES["invalid_format"].format(line))
    except FileNotFoundError:
        print(ERRORS["file_not_found"])
    return grid


def writing_grid(grid: Grid, filename: str) -> None:
    """
    Write grid configuration to a file.
    Writes coordinates of all live cells, one per line.

    Args:
        grid: Game grid to save
        filename: Path to the output file
    """
    with open(filename, 'w') as f:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 1:
                    f.write(f'{row} {col}\n')


def set_cell(grid: Grid, row: int, col: int, value: int) -> None:
    """
    Set a cell to a specific value if coordinates are valid.

    Args:
        grid: Game grid
        row: Row index
        col: Column index
        value: Value to set (0 or 1)
    """
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = value


def get_presets_names() -> List[str]:
    """
    Get list of available preset pattern names.

    Returns:
        List of preset names
    """
    return list(PRESET_PATTERNS.keys())


def load_preset(name: str, rows: int, columns: int, offset_row: int = 0,
                offset_col: int = 0) -> Grid:
    """
    Load a preset pattern into a grid.

    Args:
        name: Name of the preset pattern
        rows: Number of rows in the grid
        columns: Number of columns in the grid
        offset_row: Row offset for placing the pattern
        offset_col: Column offset for placing the pattern

    Returns:
        2D list with preset pattern placed at specified offset
    """
    if name not in PRESET_PATTERNS:
        print(ERRORS["preset_not_found"])
        return create_empty_grid(rows, columns)

    grid: Grid = create_empty_grid(rows, columns)
    for r, c in PRESET_PATTERNS[name]:
        nr: int = r + offset_row
        nc: int = c + offset_col
        if 0 <= nr < rows and 0 <= nc < columns:
            grid[nr][nc] = 1
    return grid
