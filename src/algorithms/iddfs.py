"""
Implementation of Iterative Deepening DFS (IDDFS).
Repeatedly applies Depth-Limited Search with an increasing limit.
"""

from dls import run_dls


def run_iddfs(grid_matrix, start_node, target_node, total_rows, total_cols):
    # Iterate through possible depths
    for current_max_depth in range(total_rows * total_cols):
        # Reset visual state for new iteration
        for row in grid_matrix:
            for node in row:
                if node.state_type == "EMPTY":
                    node.reset_to_empty()

        # Run DLS with current depth limit
        parent_tracker = run_dls(
            grid_matrix,
            start_node,
            target_node,
            current_max_depth,
            total_rows,
            total_cols,
        )

        if parent_tracker:
            # Reconstruct path logic
            temp_node = target_node
            while temp_node in parent_tracker:
                temp_node = parent_tracker[temp_node]
                if temp_node != start_node:
                    temp_node.mark_as_path_segment()
                yield True
            return
        yield True
