// Language: JAVA
// Algorithm: Hash Table / Dictionary
// Time Complexity: O(n)
// Space Complexity: O(n)
// Generated in 0.00s

import java.util.*;

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
