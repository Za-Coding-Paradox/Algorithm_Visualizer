"""
Implementation of Uniform Cost Search (UCS).
Expands the node with the lowest cumulative cost from the start.
"""

import heapq


def run_ucs(grid_matrix, start_node, target_node, total_rows, total_cols):
    # (cost, unique_id, node)
    priority_frontier = [(0, id(start_node), start_node)]
    parent_tracker = {}
    cumulative_costs = {start_node: 0}

    while priority_frontier:
        current_cost, _, current_active_node = heapq.heappop(priority_frontier)

        if current_active_node == target_node:
            while current_active_node in parent_tracker:
                current_active_node = parent_tracker[current_active_node]
                if current_active_node != start_node:
                    current_active_node.mark_as_path_segment()
                yield True
            return

        current_active_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor_candidate in current_active_node.neighbor_nodes:
            new_path_cost = current_cost + 1
            if (
                neighbor_candidate not in cumulative_costs
                or new_path_cost < cumulative_costs[neighbor_candidate]
            ):
                cumulative_costs[neighbor_candidate] = new_path_cost
                parent_tracker[neighbor_candidate] = current_active_node
                neighbor_candidate.mark_as_frontier()
                heapq.heappush(
                    priority_frontier,
                    (new_path_cost, id(neighbor_candidate), neighbor_candidate),
                )

        if current_active_node != start_node:
            current_active_node.mark_as_explored()
        yield True
