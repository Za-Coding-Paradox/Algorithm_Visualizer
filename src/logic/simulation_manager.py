"""
Logic Manager for the AI Pathfinder.
Bridges UI and Algorithms.
"""
import time
from algorithms.bfs import run_bfs
from algorithms.bidirectional import run_bidirectional
from algorithms.dfs import run_dfs
from algorithms.dls import run_dls
from algorithms.iddfs import run_iddfs
from algorithms.ucs import run_ucs


class SimulationManager:
    def __init__(self):
        self.is_running = False
        self.is_finished = False
        self.current_generator = None
        self.selected_algorithm = "BFS"
        
        # Timer variables
        self.start_time = 0
        self.duration = 0.0

        self.algorithm_map = {
            "BFS": run_bfs,
            "DFS": run_dfs,
            "UCS": run_ucs,
            "DLS": run_dls,
            "IDDFS": run_iddfs,
            "BIDIRECTIONAL": run_bidirectional
        }

    def set_algorithm(self, algorithm_name):
        if not self.is_running:
            self.selected_algorithm = algorithm_name

    def start_simulation(self, grid_matrix, start_node, target_node, rows, cols):
        if not self.is_running and start_node and target_node:
            self.is_finished = False
            self.duration = 0.0
            
            solver_function = self.algorithm_map[self.selected_algorithm]
            self.current_generator = solver_function(
                grid_matrix, start_node, target_node, rows, cols
            )
            self.is_running = True
            self.start_time = time.time() # Start Timer
            return True
        return False

    def step(self):
        if self.is_running and self.current_generator:
            try:
                next(self.current_generator)
                return True
            except StopIteration:
                self.stop_simulation()
                return False
        return False

    def stop_simulation(self):
        self.is_running = False
        self.is_finished = True
        self.duration = time.time() - self.start_time # Calculate Duration
        self.current_generator = None
