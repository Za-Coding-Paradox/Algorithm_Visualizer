from algorithms.dls import run_dls


def run_iddfs(grid_matrix, start_node, target_node, total_rows, total_cols):
    max_possible_depth = total_rows * total_cols
    for current_max_depth in range(1, max_possible_depth):
        for row in grid_matrix:
            for node in row:
                if node.state_type in ["FRONTIER", "EXPLORED", "PATH"]:
                    node.reset_to_empty()

        parent_tracker = yield from run_dls(
            grid_matrix,
            start_node,
            target_node,
            total_rows,
            total_cols,
            limit=current_max_depth,
        )

        if parent_tracker is not None:
            yield from reconstruct_final_path(parent_tracker, target_node, start_node)
            return


def reconstruct_final_path(parent_tracker, current_step, start_node):
    while current_step in parent_tracker:
        current_step = parent_tracker[current_step]
        if current_step != start_node:
            current_step.mark_as_path_segment()
        yield True
