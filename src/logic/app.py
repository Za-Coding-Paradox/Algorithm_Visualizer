"""
The Application Orchestrator.
This module manages the high-level execution flow, connecting the UI renderer,
the logic simulation engine, and the coordinate system.
"""

import random

import pygame

import utils.config as global_config
from logic.simulation_manager import SimulationManager as LogicEngine
from ui.grid import get_node_from_mouse_click, initialize_grid, render_grid_state
from ui.menu import InterfaceRenderer as ControlPanel


class PathfinderApp:
    """
    Main application class that handles the Pygame loop, input events,
    and coordination between the Logic Engine and UI.
    """

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (global_config.WINDOW_WIDTH, global_config.WINDOW_HEIGHT)
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
        Dispatches event handling based on the current state.
        Locks grid interaction if the simulation is running or finished.
        """
        for active_event in pygame.event.get():
            if active_event.type == pygame.QUIT:
                self.is_application_active = False

            # Lock grid interaction if Running or Finished
            if (
                not self.logic_orchestrator.is_running
                and not self.logic_orchestrator.is_finished
            ):
                self._handle_grid_interactions()

            self._handle_keyboard_commands(active_event)

    def _handle_grid_interactions(self):
        """
        Translates mouse clicks into node state changes (Start, Target, Walls).
        """
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

        if pygame.mouse.get_pressed()[0]:
            if not self.origin_node and current_node != self.destination_node:
                self.origin_node = current_node
                self.origin_node.set_as_start()
            elif not self.destination_node and current_node != self.origin_node:
                self.destination_node = current_node
                self.destination_node.set_as_target()
            elif current_node not in [self.origin_node, self.destination_node]:
                current_node.set_as_wall()

        elif pygame.mouse.get_pressed()[2]:
            if current_node == self.origin_node:
                self.origin_node = None
            elif current_node == self.destination_node:
                self.destination_node = None
            current_node.reset_to_empty()

    def _handle_keyboard_commands(self, active_event):
        """
        Maps keyboard inputs to actions.
        'C' resets the app. 1-6 select algorithms. SPACE starts simulation.
        """
        if active_event.type == pygame.KEYDOWN:
            if active_event.key == pygame.K_c:
                self._reinitialize_workspace()
                self.logic_orchestrator.is_finished = False
                return

            # Disable controls if Running or Finished
            if (
                not self.logic_orchestrator.is_running
                and not self.logic_orchestrator.is_finished
            ):
                algorithm_key_map = {
                    pygame.K_1: "BFS",
                    pygame.K_2: "DFS",
                    pygame.K_3: "UCS",
                    pygame.K_4: "DLS",
                    pygame.K_5: "IDDFS",
                    pygame.K_6: "BIDIRECTIONAL",
                }

                if active_event.key in algorithm_key_map:
                    self.logic_orchestrator.set_algorithm(
                        algorithm_key_map[active_event.key]
                    )

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
        Clears all objects from the grid and resets anchors.
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
        Randomly spawns an obstacle.
        Triggers re-planning ONLY if the obstacle blocks a Frontier or Explored node.
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
        The core application loop.
        Manages rendering, logic updates, and dynamic events.
        """
        while self.is_application_active:
            self.display_surface.fill(global_config.COLOR_BG)

            if self.logic_orchestrator.is_running:
                self.logic_orchestrator.step()

                if random.random() < global_config.DYNAMIC_SPAWN_CHANCE:
                    self._spawn_dynamic_obstacle()

            render_grid_state(self.display_surface, self.grid_matrix)

            if self.logic_orchestrator.is_running:
                status = "RUNNING"
            elif self.logic_orchestrator.is_finished:
                status = "FINISHED"
            else:
                status = "IDLE"

            self.ui_renderer.render_control_panel(
                self.logic_orchestrator.selected_algorithm, status
            )

            self._process_user_inputs()
            pygame.display.flip()
            self.execution_clock.tick(global_config.FPS)

        pygame.quit()
