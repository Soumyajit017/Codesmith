// Language: CPP
// Algorithm: Hash Table / Dictionary
// Time Complexity: O(n)
// Space Complexity: O(n)
// Generated in 0.00s

#include <iostream>
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
