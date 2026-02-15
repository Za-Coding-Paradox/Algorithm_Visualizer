"""
Logic Manager for the AI Pathfinder.
This module bridges the UI (Grid) and the Search Algorithms,
managing the execution of the selected solver.
"""

from algorithms.bfs import run_bfs
from algorithms.bidirectional import run_bidirectional
from algorithms.dfs import run_dfs
from algorithms.iddfs import run_iddfs
from algorithms.ucs import run_ucs


class SimulationManager:
    def __init__(self):
        # State tracking
        self.is_running = False
        self.current_generator = None
        self.selected_algorithm = "BFS"

        # Mapping UI names to the actual functions
        self.algorithm_map = {
            "BFS": run_bfs,
            "DFS": run_dfs,
            "UCS": run_ucs,
            "IDDFS": run_iddfs,
            "BIDIRECTIONAL": run_bidirectional,
        }

    def set_algorithm(self, algorithm_name):
        """Allows the UI to switch the active algorithm before starting."""
        if not self.is_running and algorithm_name in self.algorithm_map:
            self.selected_algorithm = algorithm_name
            print(f"Algorithm switched to: {self.selected_algorithm}")

    def start_simulation(self, grid_matrix, start_node, target_node, rows, cols):
        """Initializes the generator for the selected algorithm."""
        if not self.is_running and start_node and target_node:
            solver_function = self.algorithm_map[self.selected_algorithm]

            # Create the generator instance
            self.current_generator = solver_function(
                grid_matrix, start_node, target_node, rows, cols
            )
            self.is_running = True
            return True
        return False

    def step(self):
        """
        Executes one 'frame' of the algorithm.
        Called inside the main Pygame loop.
        """
        if self.is_running and self.current_generator:
            try:
                # Run until the next 'yield True' in the algorithm file
                next(self.current_generator)
                return True
            except StopIteration:
                # Generator has finished (path found or no path exists)
                self.stop_simulation()
                return False
        return False

    def stop_simulation(self):
        self.is_running = False
        self.current_generator = None

    def reset_grid_visuals(self, grid_matrix):
        """Clears explored/frontier colors but keeps walls/start/target."""
        if not self.is_running:
            for row in grid_matrix:
                for node in row:
                    if node.state_type not in ["WALL", "START", "TARGET", "DYNAMIC"]:
                        node.reset_to_empty()
