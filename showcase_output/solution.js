// Language: JAVASCRIPT
// Algorithm: Hash Table / Dictionary
// Time Complexity: O(n)
// Space Complexity: O(n)
// Generated in 0.00s

const readline = require('readline');

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
