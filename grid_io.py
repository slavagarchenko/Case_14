
import random
from constants import RANDOM_PROB
from ru_local import FILES, ERRORS

PRESET_PATTERNS = {'block': [(0, 0), (0, 1), (1, 0), (1, 1)]}


def create_empty_grid(rows, columns):
    """
    Create a grid filled with zeros.

    Args:
        rows: Number of rows
        columns: Number of columns

    Returns:
        2D list representing empty grid
    """
    return [[0] * columns for _ in range(rows)]


def random_grid(rows, columns, prob=RANDOM_PROB):
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
    grid = create_empty_grid(rows, columns)
    for row in range(rows):
        for col in range(columns):
            if random.random() < prob:
                grid[row][col] = 1
            else:
                grid[row][col] = 0
    return grid


def reading_grid(filename, rows, columns):
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
    grid = create_empty_grid(rows, columns)
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) == 2:
                    r, c = int(parts[0]), int(parts[1])
                    if 0 <= r < rows and 0 <= c < columns:
                        grid[r][c] = 1
                    else:
                        print(FILES["invalid_format"].format(line))
    except FileNotFoundError:
        print(ERRORS["file_not_found"])
    return grid


def writing_grid(grid, filename):
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


def set_cell(grid, row, col, value):
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


def get_presets_names():
    """
    Get list of available preset pattern names.

    Returns:
        List of preset names
    """
    return list(PRESET_PATTERNS.keys())


def load_preset(name, rows, columns, offset_row=0, offset_col=0):
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
    grid = create_empty_grid(rows, columns)
    for r, c in PRESET_PATTERNS[name]:
        nr, nc = r + offset_row, c + offset_col
        if 0 <= nr < rows and 0 <= nc < columns:
            grid[nr][nc] = 1
    return grid
