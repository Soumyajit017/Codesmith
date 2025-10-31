"""
Language-specific code templates for multi-language generation.
"""

# Python templates
PYTHON_TWO_SUM = '''import sys

def two_sum(nums, target):
    """Find two numbers that add up to target.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    Algorithm: Hash Table
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

if __name__ == '__main__':
    nums = list(map(int, sys.stdin.readline().strip().split(',')))
    target = int(sys.stdin.readline().strip())
    result = two_sum(nums, target)
    print(' '.join(map(str, result)))
'''

# C++ templates
CPP_TWO_SUM = '''#include <iostream>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <string>

using namespace std;

/*
 * Find two numbers that add up to target
 * Time Complexity: O(n)
 * Space Complexity: O(n)
 * Algorithm: Hash Table
 */
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.find(complement) != seen.end()) {
            return {seen[complement], i};
        }
        seen[nums[i]] = i;
    }
    return {};
}

int main() {
    string line;
    getline(cin, line);
    
    vector<int> nums;
    stringstream ss(line);
    string num;
    while (getline(ss, num, ',')) {
        nums.push_back(stoi(num));
    }
    
    int target;
    cin >> target;
    
    vector<int> result = twoSum(nums, target);
    if (!result.empty()) {
        cout << result[0] << " " << result[1] << endl;
    }
    
    return 0;
}
'''

# Java templates
JAVA_TWO_SUM = '''import java.util.*;

/**
 * Find two numbers that add up to target
 * Time Complexity: O(n)
 * Space Complexity: O(n)
 * Algorithm: Hash Table
 */
public class Solution {
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[]{seen.get(complement), i};
            }
            seen.put(nums[i], i);
        }
        return new int[]{};
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        String[] numsStr = scanner.nextLine().split(",");
        int[] nums = new int[numsStr.length];
        for (int i = 0; i < numsStr.length; i++) {
            nums[i] = Integer.parseInt(numsStr[i].trim());
        }
        
        int target = scanner.nextInt();
        
        int[] result = twoSum(nums, target);
        if (result.length > 0) {
            System.out.println(result[0] + " " + result[1]);
        }
        
        scanner.close();
    }
}
'''

# JavaScript templates
JS_TWO_SUM = '''const readline = require('readline');

/**
 * Find two numbers that add up to target
 * Time Complexity: O(n)
 * Space Complexity: O(n)
 * Algorithm: Hash Table
 */
function twoSum(nums, target) {
    const seen = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(nums[i], i);
    }
    return [];
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const lines = [];
rl.on('line', (line) => {
    lines.push(line);
    if (lines.length === 2) {
        const nums = lines[0].split(',').map(x => parseInt(x.trim()));
        const target = parseInt(lines[1]);
        const result = twoSum(nums, target);
        console.log(result.join(' '));
        rl.close();
    }
});
'''

# Python Number of Islands
PYTHON_NUM_ISLANDS = '''import sys
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
'''

# C++ Number of Islands
CPP_NUM_ISLANDS = '''#include <iostream>
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
'''

# Java Number of Islands
JAVA_NUM_ISLANDS = '''import java.util.*;

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
'''

# JavaScript Number of Islands
JS_NUM_ISLANDS = '''const readline = require('readline');

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
'''

TEMPLATES = {
    'python': {
        'two_sum': PYTHON_TWO_SUM,
        'num_islands': PYTHON_NUM_ISLANDS,
    },
    'cpp': {
        'two_sum': CPP_TWO_SUM,
        'num_islands': CPP_NUM_ISLANDS,
    },
    'java': {
        'two_sum': JAVA_TWO_SUM,
        'num_islands': JAVA_NUM_ISLANDS,
    },
    'javascript': {
        'two_sum': JS_TWO_SUM,
        'num_islands': JS_NUM_ISLANDS,
    }
}

def get_template(language: str, problem_type: str) -> str | None:
    """Get code template for specific language and problem."""
    if language in TEMPLATES and problem_type in TEMPLATES[language]:
        return TEMPLATES[language][problem_type]
    return None
