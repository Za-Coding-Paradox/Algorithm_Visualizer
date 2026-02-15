"""
The Application Orchestrator.
Manages execution flow, window resizing, and button interactions.
"""

import random

import pygame

import utils.config as global_config
from logic.simulation_manager import SimulationManager as LogicEngine
from ui.grid import get_node_from_mouse_click, initialize_grid, render_grid_state
from ui.menu import InterfaceRenderer as ControlPanel


class PathfinderApp:
    """
    Main application class. Handles Loop, Events, and Orchestration.
    """

    def __init__(self):
        pygame.init()
        # Initialize with Resizable Flag
        self.display_surface = pygame.display.set_mode(
            (global_config.WINDOW_WIDTH, global_config.WINDOW_HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("GOOD PERFORMANCE TIME APP")
        self.execution_clock = pygame.time.Clock()

        self.grid_matrix = initialize_grid(
            global_config.GRID_SIZE,
            global_config.GRID_SIZE,
            global_config.CELL_SIZE,
            global_config.GRID_OFFSET_X,
            global_config.GRID_OFFSET_Y,
        )
        self.logic_orchestrator = LogicEngine()
        self.ui_renderer = ControlPanel(self.display_surface)

        self.origin_node = None
        self.destination_node = None
        self.is_application_active = True

    def _process_user_inputs(self):
        """
        Handles Mouse Clicks (Menu & Grid), Keyboard, and Window Resizing.
        """
        for active_event in pygame.event.get():
            if active_event.type == pygame.QUIT:
                self.is_application_active = False

            # Handle Window Resize
            if active_event.type == pygame.VIDEORESIZE:
                self.display_surface = pygame.display.set_mode(
                    (active_event.w, active_event.h), pygame.RESIZABLE
                )
                # Re-initialize UI renderer to handle new dimensions if needed
                self.ui_renderer.target_surface = self.display_surface

            # Mouse Interactions
            if active_event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check Menu Buttons first (Always clickable unless running)
                if not self.logic_orchestrator.is_running:
                    clicked_algo = self.ui_renderer.check_button_clicks(mouse_pos)
                    if clicked_algo:
                        self.logic_orchestrator.set_algorithm(clicked_algo)

            # Grid Interactions (Only if not running/finished)
            if (
                not self.logic_orchestrator.is_running
                and not self.logic_orchestrator.is_finished
            ):
                self._handle_grid_interactions()

            # Keyboard Commands
            self._handle_keyboard_commands(active_event)

    def _handle_grid_interactions(self):
        """
        Translates mouse actions on the grid.
        """
        mouse_pixel_position = pygame.mouse.get_pos()
        # Only process if mouse is within grid bounds (approx check to save perf)
        if mouse_pixel_position[0] < 800:
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

            if pygame.mouse.get_pressed()[0]:  # Left Click
                if not self.origin_node and current_node != self.destination_node:
                    self.origin_node = current_node
                    self.origin_node.set_as_start()
                elif not self.destination_node and current_node != self.origin_node:
                    self.destination_node = current_node
                    self.destination_node.set_as_target()
                elif current_node not in [self.origin_node, self.destination_node]:
                    current_node.set_as_wall()

            elif pygame.mouse.get_pressed()[2]:  # Right Click
                if current_node == self.origin_node:
                    self.origin_node = None
                elif current_node == self.destination_node:
                    self.destination_node = None
                current_node.reset_to_empty()

    def _handle_keyboard_commands(self, active_event):
        """
        Keyboard Shortcuts.
        """
        if active_event.type == pygame.KEYDOWN:
            if active_event.key == pygame.K_c:
                self._reinitialize_workspace()
                self.logic_orchestrator.is_finished = False
                return

            if (
                not self.logic_orchestrator.is_running
                and not self.logic_orchestrator.is_finished
            ):
                if active_event.key == pygame.K_SPACE:
                    if self.origin_node and self.destination_node:
                        self.logic_orchestrator.start_simulation(
                            self.grid_matrix,
                            self.origin_node,
                            self.destination_node,
                            global_config.GRID_SIZE,
                            global_config.GRID_SIZE,
                        )

    def _reinitialize_workspace(self):
        """
        Resets the application state.
        """
        self.grid_matrix = initialize_grid(
            global_config.GRID_SIZE,
            global_config.GRID_SIZE,
            global_config.CELL_SIZE,
            global_config.GRID_OFFSET_X,
            global_config.GRID_OFFSET_Y,
        )
        self.origin_node = None
        self.destination_node = None

    def _spawn_dynamic_obstacle(self):
        """
        Handles dynamic obstacle spawning.
        """
        row = random.randint(0, global_config.GRID_SIZE - 1)
        col = random.randint(0, global_config.GRID_SIZE - 1)
        node = self.grid_matrix[row][col]

        if node.state_type not in ["START", "TARGET", "WALL", "DYNAMIC"]:
            must_replan = node.state_type in ["FRONTIER", "EXPLORED"]
            node.set_as_dynamic_obstacle()
            if must_replan:
                self.logic_orchestrator.replan(
                    self.grid_matrix, self.origin_node, self.destination_node
                )

    def run(self):
        """
        Main Loop.
        """
        while self.is_application_active:
            self.display_surface.fill(global_config.COLOR_BG)

            # Logic Step
            if self.logic_orchestrator.is_running:
                self.logic_orchestrator.step()
                if random.random() < global_config.DYNAMIC_SPAWN_CHANCE:
                    self._spawn_dynamic_obstacle()

            # Render Layers
            render_grid_state(self.display_surface, self.grid_matrix)

            # Determine Status
            if self.logic_orchestrator.is_running:
                status = "RUNNING"
            elif self.logic_orchestrator.is_finished:
                status = "FINISHED"
            else:
                status = "IDLE"

            # Render UI
            self.ui_renderer.render_control_panel(
                self.logic_orchestrator.selected_algorithm, status
            )

            # Render Pop-up if Finished
            if self.logic_orchestrator.is_finished:
                # Determine success based on target node state
                success = False
                if self.destination_node and self.destination_node.state_type in [
                    "TARGET",
                    "PATH",
                ]:
                    # BFS/DFS etc usually color the path at the end.
                    # If the target is connected to a path, we consider it success.
                    # Or simpler: check if the 'Path' color is adjacent or target is reached.
                    # The algorithms implemented previously call 'reconstruct_path' which draws.
                    success = True  # Assuming if it finished naturally, it found a path or exhausted.
                    # To be precise: If finished and NO path found, it just stops.
                    # We can check if any node is colored 'PATH'.

                    has_path = any(
                        node.current_color == global_config.COLOR_PATH
                        for row in self.grid_matrix
                        for node in row
                    )
                    success = has_path

                self.ui_renderer.render_result_popup(success)

            self._process_user_inputs()
            pygame.display.flip()
            self.execution_clock.tick(global_config.FPS)

        pygame.quit()
