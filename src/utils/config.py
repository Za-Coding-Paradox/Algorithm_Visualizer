import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60

GRID_SIZE = 25  # Number of rows/cols
CELL_SIZE = 20  # Pixels per cell
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 50

COLOR_BG = pygame.Color("#1e1e2e")  # Dark Background
COLOR_GRID = pygame.Color("#313244")  # Grid Lines
COLOR_EMPTY = pygame.Color("#45475a")  # Empty Cell
COLOR_WALL = pygame.Color("#11111b")  # Static Wall
COLOR_DYNAMIC = pygame.Color("#f38ba8")  # Red
COLOR_START = pygame.Color("#a6e3a1")  # Green
COLOR_TARGET = pygame.Color("#fab387")  # Orange
COLOR_FRONTIER = pygame.Color("#f9e2af")  # Nodes in Queue (Yellow)
COLOR_EXPLORED = pygame.Color("#89b4fa")  # Visited Nodes (Blue)
COLOR_PATH = pygame.Color("#f5c2e7")  # Final Path (Pink)

DYNAMIC_SPAWN_CHANCE = 0.01  # 5% chance per step
STEP_DELAY = 0.05
