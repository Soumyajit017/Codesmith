// Language: JAVASCRIPT
// Algorithm: Depth-First Search (DFS)
// Time Complexity: O(m*n)
// Space Complexity: O(m*n)
// Generated in 0.00s

const readline = require('readline');

/**
 * Count number of islands using DFS
 * Time Complexity: O(m * n)
 * Space Complexity: O(m * n)
 * Algorithm: Depth-First Search (DFS)
 */
function numIslands(grid) {
    if (!grid || grid.length === 0) return 0;
    
    const rows = grid.length;
    const cols = grid[0].length;
    const visited = new Set();
    let islands = 0;
    
    function dfs(r, c) {
        const key = `${r},${c}`;
        if (r < 0 || r >= rows || c < 0 || c >= cols || 
            grid[r][c] === '0' || visited.has(key)) {
            return;
        }
        
        visited.add(key);
        dfs(r + 1, c);
        dfs(r - 1, c);
        dfs(r, c + 1);
        dfs(r, c - 1);
    }
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (grid[r][c] === '1' && !visited.has(`${r},${c}`)) {
                dfs(r, c);
                islands++;
            }
        }
    }
    
    return islands;
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (line) => {
    const grid = JSON.parse(line);
    const result = numIslands(grid);
    console.log(result);
    rl.close();
});
