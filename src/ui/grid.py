"""
Grid definition for the AI Pathfinder.
"""
import pygame
import random
from utils.config import (
    COLOR_EMPTY, COLOR_EXPLORED, COLOR_FRONTIER, COLOR_GRID,
    COLOR_PATH, COLOR_START, COLOR_TARGET, COLOR_WALL
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
        self.weight = random.randint(1, 5)

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
        STRICT_MOVEMENT_ORDER = [
            (-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)
        ]

        for row_change, col_change in STRICT_MOVEMENT_ORDER:
            target_row = self.row + row_change
            target_col = self.col + col_change

            if 0 <= target_row < total_rows and 0 <= target_col < total_cols:
                potential_neighbor = grid_matrix[target_row][target_col]

                if not potential_neighbor.is_barrier():
                    if row_change != 0 and col_change != 0:
                        node_a = grid_matrix[self.row][target_col]
                        node_b = grid_matrix[target_row][self.col]
                        if node_a.is_barrier() or node_b.is_barrier():
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


def render_grid_state(surface, grid_matrix, active_algorithm=None):
    """
    Renders grid nodes. 
    If active_algorithm is 'UCS', it also renders the weight numbers.
    """
    # Create font only if needed (for performance, normally init once, but this is fine)
    weight_font = None
    if active_algorithm == "UCS":
        weight_font = pygame.font.SysFont("JetBrainsMono Nerd Font", 12, bold=True)

    for row in grid_matrix:
        for node in row:
            node.render(surface)
            
            # RENDER WEIGHTS ONLY FOR UCS
            if active_algorithm == "UCS" and node.state_type != "WALL":
                # Choose color: Black usually, White if background is dark/Start/Target
                text_color = (0, 0, 0)
                if node.state_type in ["START", "TARGET", "WALL"]:
                     text_color = (255, 255, 255)
                
                text_surf = weight_font.render(str(node.weight), True, text_color)
                # Center text in the cell
                text_rect = text_surf.get_rect(center=(node.pixel_x + node.cell_size//2, node.pixel_y + node.cell_size//2))
                surface.blit(text_surf, text_rect)


def get_node_from_mouse_click(mouse_position, row_count, col_count, cell_size, offset_x, offset_y):
    pos_x, pos_y = mouse_position
    target_col = (pos_x - offset_x) // cell_size
    target_row = (pos_y - offset_y) // cell_size

    if 0 <= target_row < row_count and 0 <= target_col < col_count:
        return target_row, target_col
    return None
