"""
The Application Orchestrator.
This module manages the high-level execution flow, connecting the UI renderer,
the logic simulation engine, and the coordinate system.
"""

import constants as global_config
import pygame
from logic_manager import SimulationManager as LogicEngine

from ui.grid import get_node_from_mouse_click, initialize_grid, render_grid_state
from ui.menu import InterfaceRenderer as ControlPanel


class PathfinderApp:
    def __init__(self):
        # Initialize Pygame and the display window
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (global_config.WINDOW_WIDTH, global_config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("AI Pathfinder Visualization - Project Final")
        self.execution_clock = pygame.time.Clock()

        # Sub-system Component Initialization
        self.grid_matrix = initialize_grid(
            global_config.GRID_SIZE,
            global_config.GRID_SIZE,
            global_config.CELL_SIZE,
            global_config.GRID_OFFSET_X,
            global_config.GRID_OFFSET_Y,
        )
        self.logic_orchestrator = LogicEngine()
        self.ui_renderer = ControlPanel(self.display_surface)

        # Tracking variables for pathfinding anchors
        self.origin_node = None
        self.destination_node = None
        self.is_application_active = True

    def _process_user_inputs(self):
        """Dispatches event handling based on the current state of the app."""
        for active_event in pygame.event.get():
            if active_event.type == pygame.QUIT:
                self.is_application_active = False

            # Only allow grid modifications if the algorithm isn't running
            if not self.logic_orchestrator.is_running:
                self._handle_grid_interactions()
                self._handle_keyboard_commands(active_event)

    def _handle_grid_interactions(self):
        """Translates mouse clicks into node state changes."""
        mouse_pixel_position = pygame.mouse.get_pos()
        grid_coordinates = get_node_from_mouse_click(
            mouse_pixel_position,
            global_config.GRID_SIZE,
            global_config.GRID_SIZE,
            global_config.CELL_SIZE,
            global_config.GRID_OFFSET_X,
            global_config.GRID_OFFSET_Y,
        )

        if not grid_coordinates:
            return

        target_row, target_col = grid_coordinates
        current_node = self.grid_matrix[target_row][target_col]

        # Primary Click: Assign Start, then Target, then Walls
        if pygame.mouse.get_pressed()[0]:
            if not self.origin_node and current_node != self.destination_node:
                self.origin_node = current_node
                self.origin_node.set_as_start()
            elif not self.destination_node and current_node != self.origin_node:
                self.destination_node = current_node
                self.destination_node.set_as_target()
            elif current_node not in [self.origin_node, self.destination_node]:
                current_node.set_as_wall()

        # Secondary Click: Remove specific assignments
        elif pygame.mouse.get_pressed()[2]:
            if current_node == self.origin_node:
                self.origin_node = None
            elif current_node == self.destination_node:
                self.destination_node = None
            current_node.reset_to_empty()

    def _handle_keyboard_commands(self, active_event):
        """Maps specific keys to algorithm selection and execution triggers."""
        if active_event.type == pygame.KEYDOWN:
            # Algorithm Selection Mapping
            algorithm_key_map = {
                pygame.K_1: "BFS",
                pygame.K_2: "DFS",
                pygame.K_3: "UCS",
                pygame.K_4: "DLS",
                pygame.K_5: "IDDFS",
                pygame.K_6: "BIDIRECTIONAL",
            }

            if active_event.key in algorithm_key_map:
                selected_name = algorithm_key_map[active_event.key]
                self.logic_orchestrator.set_algorithm(selected_name)

            # Trigger the pathfinding sequence
            if active_event.key == pygame.K_SPACE:
                if self.origin_node and self.destination_node:
                    self.logic_orchestrator.start_simulation(
                        self.grid_matrix,
                        self.origin_node,
                        self.destination_node,
                        global_config.GRID_SIZE,
                        global_config.GRID_SIZE,
                    )

            # Reset the entire canvas
            if active_event.key == pygame.K_c:
                self._reinitialize_workspace()

    def _reinitialize_workspace(self):
        """Clears all objects from the grid and resets anchors."""
        self.grid_matrix = initialize_grid(
            global_config.GRID_SIZE,
            global_config.GRID_SIZE,
            global_config.CELL_SIZE,
            global_config.GRID_OFFSET_X,
            global_config.GRID_OFFSET_Y,
        )
        self.origin_node = None
        self.destination_node = None

    def run(self):
        """The core application heartbeat."""
        while self.is_application_active:
            # Clear screen with background color
            self.display_surface.fill(global_config.COLOR_BG)

            # Step 1: Progression Logic (if simulation is active)
            if self.logic_orchestrator.is_running:
                self.logic_orchestrator.step()

            # Step 2: Visualization Layer
            render_grid_state(self.display_surface, self.grid_matrix)

            # Step 3: UI/Control Layer
            current_execution_status = (
                "RUNNING" if self.logic_orchestrator.is_running else "IDLE"
            )
            self.ui_renderer.render_control_panel(
                self.logic_orchestrator.selected_algorithm, current_execution_status
            )

            # Step 4: Input Processing
            self._process_user_inputs()

            # Maintain targeted Frame Rate
            pygame.display.flip()
            self.execution_clock.tick(global_config.FPS)

        pygame.quit()
