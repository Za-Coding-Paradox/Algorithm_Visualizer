def run_dfs(grid_matrix, start_node, target_node, total_rows, total_cols):
    nodes_to_visit_stack = [start_node]
    parent_tracker = {}
    nodes_already_visited = {start_node}

    while nodes_to_visit_stack:
        current_active_node = nodes_to_visit_stack.pop()

        if current_active_node == target_node:
            # Use 'yield from'
            yield from reconstruct_final_path(parent_tracker, target_node, start_node)
            return

        if current_active_node != start_node:
            current_active_node.mark_as_explored()

        current_active_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor_candidate in current_active_node.neighbor_nodes:
            if neighbor_candidate not in nodes_already_visited:
                nodes_already_visited.add(neighbor_candidate)
                parent_tracker[neighbor_candidate] = current_active_node
                neighbor_candidate.mark_as_frontier()
                nodes_to_visit_stack.append(neighbor_candidate)

        yield True


def reconstruct_final_path(parent_tracker, current_step, start_node):
    while current_step in parent_tracker:
        current_step = parent_tracker[current_step]
        if current_step != start_node:
            current_step.mark_as_path_segment()
        yield True
