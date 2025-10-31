// Language: JAVA
// Algorithm: Depth-First Search (DFS)
// Time Complexity: O(m*n)
// Space Complexity: O(m*n)
// Generated in 0.00s

import java.util.*;

/**
 * Count number of islands using DFS
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 * Algorithm: Depth-First Search (DFS)
 */
public class Solution {
    private int rows, cols;
    private Set<String> visited;
    
    private void dfs(char[][] grid, int r, int c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || 
            grid[r][c] == '0' || visited.contains(r + "," + c)) {
            return;
        }
        
        visited.add(r + "," + c);
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
    
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        rows = grid.length;
        cols = grid[0].length;
        visited = new HashSet<>();
        int islands = 0;
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1' && !visited.contains(r + "," + c)) {
                    dfs(grid, r, c);
                    islands++;
                }
            }
        }
        return islands;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        
        // Parse JSON-like input
        // In production, use Gson or Jackson
        
        Solution sol = new Solution();
        // char[][] grid = parseGrid(input);
        // int result = sol.numIslands(grid);
        // System.out.println(result);
        
        scanner.close();
    }
}
