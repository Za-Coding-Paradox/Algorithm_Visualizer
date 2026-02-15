"""
Logic Manager for the AI Pathfinder.
This module bridges the UI (Grid) and the Search Algorithms,
managing the execution of the selected solver.
"""

from algorithms.bfs import run_bfs
from algorithms.bidirectional import run_bidirectional
from algorithms.dfs import run_dfs
from algorithms.dls import run_dls
from algorithms.iddfs import run_iddfs
from algorithms.ucs import run_ucs


class SimulationManager:
    """
    Controls the state of the search algorithm (Running, Finished, Idle).
    Handles starting, stopping, stepping, and re-planning the search.
    """

    def __init__(self):
        self.is_running = False
        self.is_finished = False
        self.current_generator = None
        self.selected_algorithm = "BFS"

        self.algorithm_map = {
            "BFS": run_bfs,
            "DFS": run_dfs,
            "UCS": run_ucs,
            "DLS": run_dls,
            "IDDFS": run_iddfs,
            "BIDIRECTIONAL": run_bidirectional,
        }

    def set_algorithm(self, algorithm_name):
        """
        Updates the selected algorithm if the simulation is idle.
        """
        if not self.is_running:
            self.selected_algorithm = algorithm_name
            print(f"Algorithm switched to: {self.selected_algorithm}")

    def start_simulation(self, grid_matrix, start_node, target_node, rows, cols):
        """
        Initializes the generator for the selected algorithm and starts the run state.
        """
        if not self.is_running and start_node and target_node:
            self.is_finished = False
            solver_function = self.algorithm_map[self.selected_algorithm]

            self.current_generator = solver_function(
                grid_matrix, start_node, target_node, rows, cols
            )
            self.is_running = True
            return True
        return False

    def step(self):
        """
        Advances the algorithm generator by one step.
        Marks simulation as finished if the generator completes.
        """
        if self.is_running and self.current_generator:
            try:
                next(self.current_generator)
                return True
            except StopIteration:
                self.stop_simulation()
                return False
        return False

    def stop_simulation(self):
        """
        Stops the running state and marks the simulation as finished.
        """
        self.is_running = False
        self.is_finished = True
        self.current_generator = None

    def replan(self, grid_matrix, start_node, target_node):
        """
        Handles dynamic obstacles by stopping, cleaning the grid, and restarting.
        Does NOT mark as finished, allowing the loop to continue.
        """
        print("CRITICAL BLOCKAGE! Re-planning path...")
        self.stop_simulation()
        self.is_finished = False

        for row in grid_matrix:
            for node in row:
                if node.state_type == "DYNAMIC":
                    node.set_as_wall()
                elif node.state_type in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.reset_to_empty()

        rows = len(grid_matrix)
        cols = len(grid_matrix[0])
        self.start_simulation(grid_matrix, start_node, target_node, rows, cols)
