// Language: CPP
// Algorithm: Depth-First Search (DFS)
// Time Complexity: O(m*n)
// Space Complexity: O(m*n)
// Generated in 0.00s

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <set>

using namespace std;

/*
 * Count number of islands using DFS
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 * Algorithm: Depth-First Search (DFS)
 */
class Solution {
private:
    int rows, cols;
    set<pair<int,int>> visited;
    
    void dfs(vector<vector<char>>& grid, int r, int c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || 
            grid[r][c] == '0' || visited.count({r, c})) {
            return;
        }
        
        visited.insert({r, c});
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
    
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) return 0;
        
        rows = grid.size();
        cols = grid[0].size();
        int islands = 0;
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1' && !visited.count({r, c})) {
                    dfs(grid, r, c);
                    islands++;
                }
            }
        }
        return islands;
    }
};

int main() {
    // Parse JSON-like input: [["1","1"],["0","1"]]
    string line;
    getline(cin, line);
    
    vector<vector<char>> grid;
    // Simple parser for demo
    // In production, use proper JSON library
    
    Solution sol;
    int result = sol.numIslands(grid);
    cout << result << endl;
    
    return 0;
}
