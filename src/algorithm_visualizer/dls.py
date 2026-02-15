"""
Implementation of Depth-Limited Search (DLS).
Limits the search depth to prevent infinite paths in DFS.
"""


def run_dls(grid_matrix, start_node, target_node, depth_limit, total_rows, total_cols):
    return _dls_recursive(
        start_node,
        target_node,
        depth_limit,
        {},
        {start_node},
        grid_matrix,
        total_rows,
        total_cols,
    )


def _dls_recursive(current, target, limit, parent_tracker, visited, grid, rows, cols):
    if current == target:
        return parent_tracker
    if limit <= 0:
        return None

    current.identify_neighbors(grid, rows, cols)
    for neighbor in current.neighbor_nodes:
        if neighbor not in visited:
            visited.add(neighbor)
            parent_tracker[neighbor] = current
            neighbor.mark_as_frontier()

            result = _dls_recursive(
                neighbor, target, limit - 1, parent_tracker, visited, grid, rows, cols
            )
            if result:
                return result
    return None
