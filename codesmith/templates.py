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

TEMPLATES = {
    'python': {
        'two_sum': PYTHON_TWO_SUM,
    },
    'cpp': {
        'two_sum': CPP_TWO_SUM,
    },
    'java': {
        'two_sum': JAVA_TWO_SUM,
    },
    'javascript': {
        'two_sum': JS_TWO_SUM,
    }
}

def get_template(language: str, problem_type: str) -> str | None:
    """Get code template for specific language and problem."""
    if language in TEMPLATES and problem_type in TEMPLATES[language]:
        return TEMPLATES[language][problem_type]
    return None
