"""
Implementation of Iterative Deepening DFS (IDDFS).
Repeatedly applies Depth-Limited Search with an increasing limit.
"""

from algorithms.dls import run_dls


def run_iddfs(grid_matrix, start_node, target_node, total_rows, total_cols):
    # Iterate through possible depths
    # Start from depth 1 up to max possible path length
    for current_max_depth in range(1, total_rows * total_cols):
        # Reset Frontier/Explored from the previous depth iteration
        # We must keep Walls, Start, Target, and Dynamic obstacles intact.
        for row in grid_matrix:
            for node in row:
                if node.state_type in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.reset_to_empty()

        # Run DLS with current depth limit
        # Use 'yield from' to delegate execution to DLS and capture the result
        parent_tracker = yield from run_dls(
            grid_matrix,
            start_node,
            target_node,
            current_max_depth,
            total_rows,
            total_cols,
        )

        # If DLS returns a parent_tracker, it means a path was found
        if parent_tracker:
            temp_node = target_node
            while temp_node in parent_tracker:
                temp_node = parent_tracker[temp_node]
                if temp_node != start_node:
                    temp_node.mark_as_path_segment()
                yield True
            return  # Exit once path is found

        # Yield to allow UI update between depth increases
        yield True
