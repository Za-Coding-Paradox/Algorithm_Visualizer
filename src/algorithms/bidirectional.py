from collections import deque


def run_bidirectional(grid_matrix, start_node, target_node, total_rows, total_cols):
    start_frontier = deque([start_node])
    target_frontier = deque([target_node])

    start_parent_map = {}
    target_parent_map = {}

    start_visited = {start_node}
    target_visited = {target_node}

    while start_frontier and target_frontier:
        # Start Side
        current_start_node = start_frontier.popleft()
        if current_start_node != start_node:
            current_start_node.mark_as_explored()
        current_start_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_start_node.neighbor_nodes:
            if neighbor in target_visited:
                start_parent_map[neighbor] = current_start_node
                yield from _reconstruct_bidirectional(
                    start_parent_map,
                    target_parent_map,
                    neighbor,
                    start_node,
                    target_node,
                )
                return
            if neighbor not in start_visited:
                start_visited.add(neighbor)
                start_parent_map[neighbor] = current_start_node
                neighbor.mark_as_frontier()
                start_frontier.append(neighbor)

        # Target Side
        current_target_node = target_frontier.popleft()
        if current_target_node != target_node:
            current_target_node.mark_as_explored()
        current_target_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_target_node.neighbor_nodes:
            if neighbor in start_visited:
                target_parent_map[neighbor] = current_target_node
                yield from _reconstruct_bidirectional(
                    start_parent_map,
                    target_parent_map,
                    neighbor,
                    start_node,
                    target_node,
                )
                return
            if neighbor not in target_visited:
                target_visited.add(neighbor)
                target_parent_map[neighbor] = current_target_node
                neighbor.mark_as_frontier()
                target_frontier.append(neighbor)
        yield True


def _reconstruct_bidirectional(start_map, target_map, meeting_node, start, target):
    if meeting_node != start and meeting_node != target:
        meeting_node.mark_as_path_segment()
    yield True

    curr = meeting_node
    while curr in start_map:
        curr = start_map[curr]
        if curr != start:
            curr.mark_as_path_segment()
        yield True

    curr = meeting_node
    while curr in target_map:
        curr = target_map[curr]
        if curr != target:
            curr.mark_as_path_segment()
        yield True
