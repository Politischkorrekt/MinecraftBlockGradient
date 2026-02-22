import numpy as np

def find_blocks(first, last, intermediate_steps, block_dict):
    """
    Finds the smoothest possible path between two blocks using Dynamic Programming
    and squared color distances to penalize harsh color jumps.
    """
    nodes = list(block_dict.keys())
    
    # If we want 10 intermediate blocks, we are making 11 jumps (transitions)
    total_jumps = intermediate_steps + 1
    
    # DP table: dp[jumps_taken][current_block] = (total_cost, previous_block)
    # We start with infinite cost for everything
    dp = {i: {node: (float('inf'), None) for node in nodes} for i in range(total_jumps + 1)}
    
    # Starting point costs 0
    dp[0][first] = (0, None)
    
    for jump in range(1, total_jumps + 1):
        for current_block in nodes:
            best_cost = float('inf')
            best_parent = None
            current_arr = np.array(block_dict[current_block])
            
            for prev_block in nodes:
                # If we haven't reached this previous block yet, skip it
                if dp[jump-1][prev_block][0] == float('inf'):
                    continue
                
                # Prevent picking the exact same block twice in a row
                if current_block == prev_block:
                    continue
                
                prev_arr = np.array(block_dict[prev_block])
                
                # THE MAGIC TRICK: Squaring the distance. 
                # This makes two small jumps much "cheaper" than one massive jump,
                # forcing the algorithm to find smooth intermediate colors.
                dist = np.linalg.norm(current_arr - prev_arr)
                jump_cost = dist ** 2 
                
                total_cost = dp[jump-1][prev_block][0] + jump_cost
                
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_parent = prev_block
                    
            dp[jump][current_block] = (best_cost, best_parent)
            
    # Reconstruct the path backwards from the 'last' block
    path = []
    current = last
    for jump in range(total_jumps, 0, -1):
        path.append(current)
        # Move backwards to the parent block that got us here
        current = dp[jump][current][1] 
        
        if current is None:
            return ["Error: No valid path found through the palette."]
            
    path.append(first)
    path.reverse() # Flip it so it goes Start -> End    
    return path


def find_blocks_range(first, last, min_steps, max_steps, block_dict):
    """
    Finds the smoothest possible path between two blocks, allowing the 
    algorithm to pick the optimal number of steps within a given range.
    """
    nodes = list(block_dict.keys())
    
    # +1 because 5 intermediate blocks = 6 actual jumps
    min_jumps = min_steps + 1
    max_jumps = max_steps + 1
    
    # DP table up to max_jumps
    dp = {i: {node: (float('inf'), None) for node in nodes} for i in range(max_jumps + 1)}
    dp[0][first] = (0, None)
    
    # 1. Calculate all possible paths up to max_jumps
    for jump in range(1, max_jumps + 1):
        for current_block in nodes:
            best_cost = float('inf')
            best_parent = None
            current_arr = np.array(block_dict[current_block])
            
            for prev_block in nodes:
                if dp[jump-1][prev_block][0] == float('inf'):
                    continue
                
                if current_block == prev_block:
                    continue
                
                prev_arr = np.array(block_dict[prev_block])
                
                # Square the distance
                dist = np.linalg.norm(current_arr - prev_arr)
                jump_cost = dist ** 2 
                
                total_cost = dp[jump-1][prev_block][0] + jump_cost
                
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_parent = prev_block
                    
            dp[jump][current_block] = (best_cost, best_parent)
            
    # 2. Look at our 'last' block and find which jump count gave the lowest cost
    best_overall_cost = float('inf')
    optimal_jumps = None
    
    for j in range(min_jumps, max_jumps + 1):
        if dp[j][last][0] < best_overall_cost:
            best_overall_cost = dp[j][last][0]
            optimal_jumps = j
            
    if optimal_jumps is None or best_overall_cost == float('inf'):
        return ["Error: No valid path found."]
        
    # 3. Reconstruct the path backwards from the optimal number of jumps
    path = []
    current = last
    for jump in range(optimal_jumps, 0, -1):
        path.append(current)
        current = dp[jump][current][1] 
        
    path.append(first)
    path.reverse()
    
    print(f"Optimal path found using {optimal_jumps - 1} intermediate steps.")
    return path
