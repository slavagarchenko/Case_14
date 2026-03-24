
# Grid dimensions
ROWS: int = 30
COLS: int = 50
CELL_SIZE: int = 20

# FPS settings
FPS: int = 10
MIN_SPEED: int = 1
MAX_SPEED: int = 60
SPEED_STEP: int = 1

# File name for save/load
FILENAME: str = "grid.txt"

# Random generation probability
RANDOM_PROB: float = 0.2

# Colors
COLOR_ALIVE: tuple[int, int, int] = (0, 255, 0)
COLOR_DEAD: tuple[int, int, int] = (0, 0, 0)
COLOR_GRID: tuple[int, int, int] = (40, 40, 40)
COLOR_FONT: tuple[int, int, int] = (255, 255, 255)

# Window title
WINDOW_TITLE: str = "Game of Life"

# Font settings
FONT_NAME: str = "Arial"
FONT_SIZE: int = 18

# Preset pattern parameters
PRESET_OFFSET_ROW: int = 0
PRESET_OFFSET_COL: int = 0

# Maximum period for oscillation detection
MAX_PERIOD: int = 10

# Default neighborhood radius
NEIGHBORHOOD_RADIUS: int = 1
