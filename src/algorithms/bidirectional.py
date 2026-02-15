"""
Implementation of Bidirectional Search.
Starts two searches: one from start to target, and another from target to start.
"""

from collections import deque


def run_bidirectional(grid_matrix, start_node, target_node, total_rows, total_cols):
    start_frontier = deque([start_node])
    target_frontier = deque([target_node])

    start_parent_map = {}
    target_parent_map = {}

    start_visited = {start_node}
    target_visited = {target_node}

    while start_frontier and target_frontier:
        # Expand from Start side
        current_start_node = start_frontier.popleft()
        current_start_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_start_node.neighbor_nodes:
            if neighbor in target_visited:  # BRIDGE FOUND
                start_parent_map[neighbor] = current_start_node
                # Connect the paths
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

        # Expand from Target side
        current_target_node = target_frontier.popleft()
        current_target_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_target_node.neighbor_nodes:
            if neighbor in start_visited:  # BRIDGE FOUND
                target_parent_map[neighbor] = current_target_node
                # Connect the paths
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
    """
    Draws the path from the middle outwards to both Start and Target.
    """
    # Mark the meeting point itself
    if meeting_node != start and meeting_node != target:
        meeting_node.mark_as_path_segment()
    yield True

    # Path back to Start
    curr = meeting_node
    while curr in start_map:
        curr = start_map[curr]
        if curr != start:
            curr.mark_as_path_segment()
        yield True

    # Path back to Target
    curr = meeting_node
    while curr in target_map:
        curr = target_map[curr]
        if curr != target:
            curr.mark_as_path_segment()
        yield True
