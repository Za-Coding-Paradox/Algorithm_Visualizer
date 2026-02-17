"""
Implementation of Uniform Cost Search (UCS).
Yields the Priority Queue nodes for sidebar visualization.
"""
import heapq

def run_ucs(grid_matrix, start_node, target_node, total_rows, total_cols):
    # Priority Queue stores tuples: (Cost, PriorityCount, Node)
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, start_node))
    
    parent_tracker = {}
    cost_so_far = {start_node: 0}
    visited_set = set()
    counter = 1

    while priority_queue:
        current_cost, _, current_active_node = heapq.heappop(priority_queue)

        if current_active_node in visited_set:
            continue
        visited_set.add(current_active_node)

        if current_active_node == target_node:
            yield from reconstruct_final_path(parent_tracker, target_node, start_node)
            return

        current_active_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_active_node.neighbor_nodes:
            # USE RANDOM WEIGHT HERE
            new_cost = current_cost + neighbor.weight 
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent_tracker[neighbor] = current_active_node
                heapq.heappush(priority_queue, (new_cost, counter, neighbor))
                counter += 1
                neighbor.mark_as_frontier()

        if current_active_node != start_node:
            current_active_node.mark_as_explored()
        yield True

def reconstruct_final_path(parent_tracker, current_step, start_node):
    while current_step in parent_tracker:
        current_step = parent_tracker[current_step]
        if current_step != start_node:
            current_step.mark_as_path_segment()
        yield True
