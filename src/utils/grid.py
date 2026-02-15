"""
Grid definition for the AI Pathfinder.
Handles the state of individual cells and the rendering logic
"""

import pygame
from constants import (
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

        # Exact pixel coordinates for Pygame rendering
        self.pixel_x = col_index * cell_size + offset_x
        self.pixel_y = row_index * cell_size + offset_y

        self.current_color = COLOR_EMPTY
        self.state_type = "EMPTY"  # Options: EMPTY, WALL, DYNAMIC, START, TARGET
        self.neighbor_nodes = []

    def get_grid_coordinates(self):
        return self.row, self.col

    # State Identification
    def is_barrier(self):
        return self.state_type == "WALL"

    def is_origin(self):
        return self.state_type == "START"

    def is_destination(self):
        return self.state_type == "TARGET"

    # Visual State Setters
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
        """Draws the node and its border onto the provided surface."""
        rect_dimensions = (self.pixel_x, self.pixel_y, self.cell_size, self.cell_size)
        pygame.draw.rect(surface, self.current_color, rect_dimensions)
        # Draw the grid line border
        pygame.draw.rect(surface, COLOR_GRID, rect_dimensions, 1)

    def identify_neighbors(self, grid_matrix, total_rows, total_cols):
        """Standard 4-way connectivity check (Up, Down, Left, Right)."""
        self.neighbor_nodes = []
        # Movement offsets: (row_change, col_change)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for row_change, col_change in directions:
            target_row = self.row + row_change
            target_col = self.col + col_change

            # Boundary Check
            if 0 <= target_row < total_rows and 0 <= target_col < total_cols:
                potential_neighbor = grid_matrix[target_row][target_col]

                # Check if the node is traversable
                if (
                    not potential_neighbor.is_barrier()
                    and potential_neighbor.state_type != "DYNAMIC"
                ):
                    self.neighbor_nodes.append(potential_neighbor)


### Grid Management Helpers


def initialize_grid(row_count, col_count, cell_size, offset_x, offset_y):
    """Generates a 2D matrix of GridNode objects."""
    grid_matrix = []
    for r in range(row_count):
        current_row = []
        for c in range(col_count):
            new_node = GridNode(r, c, cell_size, offset_x, offset_y)
            current_row.append(new_node)
        grid_matrix.append(current_row)
    return grid_matrix


def render_grid_state(surface, grid_matrix):
    """Iterates through all nodes and draws them."""
    for row in grid_matrix:
        for node in row:
            node.render(surface)
    pygame.display.flip()


def get_node_from_mouse_click(
    mouse_position, row_count, col_count, cell_size, offset_x, offset_y
):
    """Translates mouse pixel position to (row, col) grid coordinates."""
    pos_x, pos_y = mouse_position

    # Reverse the pixel math: (Pixel - Offset) / Size
    target_col = (pos_x - offset_x) // cell_size
    target_row = (pos_y - offset_y) // cell_size

    if 0 <= target_row < row_count and 0 <= target_col < col_count:
        return target_row, target_col
    return None
