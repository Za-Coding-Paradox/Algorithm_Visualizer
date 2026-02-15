"""
Grid definition for the AI Pathfinder.
Handles the state of individual cells and the rendering logic
"""

import pygame

from utils.config import (
    COLOR_DYNAMIC,
    COLOR_EMPTY,
    COLOR_EXPLORED,
    COLOR_FRONTIER,
    COLOR_GRID,
    COLOR_PATH,
    COLOR_START,
    COLOR_TARGET,
    COLOR_WALL,
)


class GridNode:
    def __init__(self, row_index, col_index, cell_size, offset_x, offset_y):
        self.row = row_index
        self.col = col_index
        self.cell_size = cell_size
        self.pixel_x = col_index * cell_size + offset_x
        self.pixel_y = row_index * cell_size + offset_y
        self.current_color = COLOR_EMPTY
        self.state_type = "EMPTY"
        self.neighbor_nodes = []

    def get_grid_coordinates(self):
        return self.row, self.col

    def is_barrier(self):
        return self.state_type == "WALL"

    def reset_to_empty(self):
        self.current_color = COLOR_EMPTY
        self.state_type = "EMPTY"

    def set_as_wall(self):
        self.current_color = COLOR_WALL
        self.state_type = "WALL"

    def set_as_dynamic_obstacle(self):
        self.current_color = COLOR_DYNAMIC
        self.state_type = "DYNAMIC"

    def set_as_start(self):
        self.current_color = COLOR_START
        self.state_type = "START"

    def set_as_target(self):
        self.current_color = COLOR_TARGET
        self.state_type = "TARGET"

    def mark_as_frontier(self):
        if self.state_type == "EMPTY":
            self.current_color = COLOR_FRONTIER

    def mark_as_explored(self):
        if self.state_type == "EMPTY":
            self.current_color = COLOR_EXPLORED

    def mark_as_path_segment(self):
        self.current_color = COLOR_PATH

    def render(self, surface):
        rect_dimensions = (self.pixel_x, self.pixel_y, self.cell_size, self.cell_size)
        pygame.draw.rect(surface, self.current_color, rect_dimensions)
        pygame.draw.rect(surface, COLOR_GRID, rect_dimensions, 1)

    def identify_neighbors(self, grid_matrix, total_rows, total_cols):
        self.neighbor_nodes = []
        # Strict Clockwise Order + Main Diagonals Only
        STRICT_MOVEMENT_ORDER = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]

        for row_change, col_change in STRICT_MOVEMENT_ORDER:
            target_row = self.row + row_change
            target_col = self.col + col_change

            if 0 <= target_row < total_rows and 0 <= target_col < total_cols:
                potential_neighbor = grid_matrix[target_row][target_col]

                # Basic Obstacle Check
                if (
                    not potential_neighbor.is_barrier()
                    and potential_neighbor.state_type != "DYNAMIC"
                ):
                    # Corner Cutting Check
                    if row_change != 0 and col_change != 0:
                        node_a = grid_matrix[self.row][target_col]
                        node_b = grid_matrix[target_row][self.col]
                        if (
                            node_a.is_barrier()
                            or node_a.state_type == "DYNAMIC"
                            or node_b.is_barrier()
                            or node_b.state_type == "DYNAMIC"
                        ):
                            continue

                    self.neighbor_nodes.append(potential_neighbor)


def initialize_grid(row_count, col_count, cell_size, offset_x, offset_y):
    grid_matrix = []
    for r in range(row_count):
        current_row = []
        for c in range(col_count):
            new_node = GridNode(r, c, cell_size, offset_x, offset_y)
            current_row.append(new_node)
        grid_matrix.append(current_row)
    return grid_matrix


def render_grid_state(surface, grid_matrix):
    """
    Draws the grid nodes AND the row/column numbering system.
    """
    font = pygame.font.SysFont("JetBrainsMono Nerd Font", 12)

    # Draw Nodes
    for row in grid_matrix:
        for node in row:
            node.render(surface)

    # Draw Column Numbers (Top)
    # Assuming all rows have same length
    if not grid_matrix:
        return

    first_row = grid_matrix[0]
    for col_idx, node in enumerate(first_row):
        text = font.render(str(col_idx), True, (150, 150, 150))
        # Position above the grid
        surface.blit(text, (node.pixel_x + 5, node.pixel_y - 15))

    # Draw Row Numbers (Left)
    for row_idx, row in enumerate(grid_matrix):
        node = row[0]
        text = font.render(str(row_idx), True, (150, 150, 150))
        # Position left of the grid
        surface.blit(text, (node.pixel_x - 20, node.pixel_y + 5))


def get_node_from_mouse_click(
    mouse_position, row_count, col_count, cell_size, offset_x, offset_y
):
    pos_x, pos_y = mouse_position
    target_col = (pos_x - offset_x) // cell_size
    target_row = (pos_y - offset_y) // cell_size

    if 0 <= target_row < row_count and 0 <= target_col < col_count:
        return target_row, target_col
    return None
