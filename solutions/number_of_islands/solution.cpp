// Language: CPP
// Algorithm: Depth-First Search (DFS)
// Time Complexity: O(m*n)
// Space Complexity: O(m*n)
// Generated in 0.00s

import sys
import json

def numIslands(grid):
    """Count number of islands using DFS.
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    Algorithm: Depth-First Search (DFS)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    visited = set()
    islands = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            grid[r][c] == '0' or (r, c) in visited):
            return
        
        visited.add((r, c))
        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                islands += 1
    
    return islands

if __name__ == '__main__':
    grid_str = sys.stdin.readline().strip()
    grid = json.loads(grid_str)
    result = numIslands(grid)
    print(result)
