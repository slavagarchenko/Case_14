from typing import List, Tuple


Grid = List[List[int]]


def count_live_neighbors(grid: Grid, row: int, col: int,
                         toroidal: bool = True) -> int:
    """
    Count the number of live neighbors around a cell.

    Args:
        grid: The game grid as 2D list of integers (0 or 1)
        row: Row index of the target cell
        col: Column index of the target cell
        toroidal: If True, grid wraps around (torus),
                  if False, edges have fewer neighbors

    Returns:
        Number of live neighbors (0-8)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows == 0 or cols == 0:
        return 0

    live_count = 0

    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == 0 and col_offset == 0:
                continue

            if toroidal:
                neighbor_row = (row + row_offset) % rows
                neighbor_col = (col + col_offset) % cols
            else:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if neighbor_row < 0 or neighbor_row >= rows or neighbor_col < 0 or neighbor_col >= cols:
                    continue

            live_count += grid[neighbor_row][neighbor_col]

    return live_count


def next_generation(grid: Grid, toroidal: bool = True) -> Grid:
    """
    Compute the next generation of cells based on Conway's rules.

    Rules:
    - Live cell with 2 or 3 live neighbors survives
    - Dead cell with exactly 3 live neighbors becomes alive
    - All other cells die or remain dead

    Args:
        grid: Current generation grid
        toroidal: If True, use toroidal boundaries,
                  if False use open boundaries

    Returns:
        New grid representing the next generation (original unchanged)
    """
    if not grid or not grid[0]:
        return []

    rows = len(grid)
    cols = len(grid[0])

    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for current_row in range(rows):
        for current_col in range(cols):
            live_neighbors = count_live_neighbors(
                grid, current_row, current_col, toroidal
            )
            current_cell = grid[current_row][current_col]

            if current_cell == 1:
                if live_neighbors in (2, 3):
                    new_grid[current_row][current_col] = 1
                else:
                    new_grid[current_row][current_col] = 0
            else:
                if live_neighbors == 3:
                    new_grid[current_row][current_col] = 1
                else:
                    new_grid[current_row][current_col] = 0

    return new_grid


def apply_boundary(row: int, col: int, rows: int, cols: int,
                   toroidal: bool = True) -> Tuple[int, int]:
    """
    Apply boundary conditions to coordinates.

    Args:
        row: Input row coordinate
        col: Input column coordinate
        rows: Total number of rows in grid
        cols: Total number of columns in grid
        toroidal: If True, wrap coordinates, if False, clamp to boundaries

    Returns:
        Tuple of (adjusted_row, adjusted_col) within grid boundaries
    """
    if toroidal:
        return row % rows, col % cols

    clamped_row = max(0, min(row, rows - 1))
    clamped_col = max(0, min(col, cols - 1))
    return clamped_row, clamped_col


def count_live_cells(grid: Grid) -> int:
    """
    Count total number of live cells in the grid.

    Args:
        grid: Game grid

    Returns:
        Number of cells with value 1
    """
    return sum(sum(row) for row in grid)


def get_live_cells(grid: Grid) -> List[Tuple[int, int]]:
    """
    Get coordinates of all live cells.

    Args:
        grid: Game grid

    Returns:
        List of (row, col) tuples for live cells
    """
    cells = []
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[0])):
            if grid[row_idx][col_idx] == 1:
                cells.append((row_idx, col_idx))
    return cells


def get_dead_cells(grid: Grid) -> List[Tuple[int, int]]:
    """
    Get coordinates of all dead cells.

    Args:
        grid: Game grid

    Returns:
        List of (row, col) tuples for dead cells
    """
    cells = []
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[0])):
            if grid[row_idx][col_idx] == 0:
                cells.append((row_idx, col_idx))
    return cells


def compare_grids(grid1: Grid, grid2: Grid) -> bool:
    """
    Compare two grids for equality.

    Args:
        grid1: First grid
        grid2: Second grid

    Returns:
        True if grids have same dimensions and all cells equal
    """
    if len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return False

    for row_idx in range(len(grid1)):
        for col_idx in range(len(grid1[0])):
            if grid1[row_idx][col_idx] != grid2[row_idx][col_idx]:
                return False

    return True


def copy_grid(grid: Grid) -> Grid:
    """
    Create a deep copy of the grid.

    Args:
        grid: Grid to copy

    Returns:
        New grid with identical cell values
    """
    return [row[:] for row in grid]


def create_pattern_grid(rows: int, cols: int, pattern: List[Tuple[int, int]],
                        offset_row: int = 0, offset_col: int = 0) -> Grid:
    """
    Create a grid with a specific pattern of live cells.

    Args:
        rows: Number of rows in new grid
        cols: Number of columns in new grid
        pattern: List of (row, col) coordinates for live cells
        offset_row: Row offset to apply to pattern coordinates
        offset_col: Column offset to apply to pattern coordinates

    Returns:
        New grid with pattern placed at specified offset
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for pattern_row, pattern_col in pattern:
        new_row = pattern_row + offset_row
        new_col = pattern_col + offset_col

        if 0 <= new_row < rows and 0 <= new_col < cols:
            grid[new_row][new_col] = 1

    return grid


def get_neighborhood(grid: Grid, row: int, col: int,
                     radius: int = 1, toroidal: bool = True) -> List[List[int]]:
    """
    Extract a square neighborhood around a cell.

    Args:
        grid: Game grid
        row: Center row
        col: Center column
        radius: Neighborhood radius (1 gives 3x3, 2 gives 5x5, etc.)
        toroidal: If True, wrap around grid boundaries

    Returns:
        2D list of cell values in the neighborhood
    """
    if radius < 0:
        return []

    rows, cols = len(grid), len(grid[0])
    size = 2 * radius + 1
    neighborhood = [[0 for _ in range(size)] for _ in range(size)]

    for row_offset in range(-radius, radius + 1):
        for col_offset in range(-radius, radius + 1):
            if toroidal:
                neighbor_row = (row + row_offset) % rows
                neighbor_col = (col + col_offset) % cols
            else:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if neighbor_row < 0 or neighbor_row >= rows or neighbor_col < 0 or neighbor_col >= cols:
                    continue

            neighborhood[row_offset + radius][col_offset + radius] = grid[neighbor_row][neighbor_col]

    return neighborhood


def detect_period(grid: Grid, max_period: int = 10,
                  toroidal: bool = True) -> int:
    """
    Detect if the pattern oscillates with a certain period.

    Args:
        grid: Initial grid state
        max_period: Maximum period to check
        toroidal: Boundary condition to use

    Returns:
        Oscillation period if found (1 to max_period), 0 if not found
    """
    if not grid or not grid[0]:
        return 0

    states = [copy_grid(grid)]

    for period in range(1, max_period + 1):
        next_state = next_generation(states[-1], toroidal)

        if compare_grids(next_state, states[0]):
            return period

        states.append(next_state)

    return 0


def evolve_for_steps(grid: Grid, steps: int,
                     toroidal: bool = True) -> List[Grid]:
    """
    Evolve the grid for a specified number of steps and return all states.

    Args:
        grid: Initial grid state
        steps: Number of generations to evolve
        toroidal: Boundary condition to use

    Returns:
        List of grid states including initial and each generation
    """
    history = [copy_grid(grid)]
    current = copy_grid(grid)

    for _ in range(steps):
        current = next_generation(current, toroidal)
        history.append(copy_grid(current))

    return history


def calculate_density(grid: Grid) -> float:
    """
    Calculate the population density.

    Args:
        grid: Game grid

    Returns:
        Float between 0.0 and 1.0 representing live cell proportion
    """
    total_cells = len(grid) * len(grid[0])
    if total_cells == 0:
        return 0.0

    live_cells = count_live_cells(grid)
    return live_cells / total_cells


def get_dimensions(grid: Grid) -> Tuple[int, int]:
    """
    Get grid dimensions.

    Args:
        grid: Game grid

    Returns:
        Tuple of (rows, columns)
    """
    if not grid:
        return 0, 0
    return len(grid), len(grid[0])


def validate_coordinates(grid: Grid, row: int, col: int) -> bool:
    """
    Check if coordinates are within grid bounds.

    Args:
        grid: Game grid
        row: Row to check
        col: Column to check

    Returns:
        True if coordinates are valid, False otherwise
    """
    rows, cols = get_dimensions(grid)
    return 0 <= row < rows and 0 <= col < cols


def get_cell_state(grid: Grid, row: int, col: int,
                   toroidal: bool = False, default: int = 0) -> int:
    """
    Get cell state with optional boundary handling.

    Args:
        grid: Game grid
        row: Row index
        col: Column index
        toroidal: If True, wrap coordinates,
                  if False, return default for out-of-bounds
        default: Default value for out-of-bounds cells when toroidal is False

    Returns:
        Cell value (0 or 1) or default value
    """
    if toroidal:
        rows, cols = get_dimensions(grid)
        if rows == 0 or cols == 0:
            return default
        wrapped_row = row % rows
        wrapped_col = col % cols
        return grid[wrapped_row][wrapped_col]

    if validate_coordinates(grid, row, col):
        return grid[row][col]
    return default
