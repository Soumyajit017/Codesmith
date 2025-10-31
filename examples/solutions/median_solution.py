import sys

def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Finds the median of two sorted arrays using a binary search approach.

    The time complexity is O(log(min(m,n))), where m and n are the lengths
    of the input arrays.

    Args:
        nums1: The first sorted list of integers.
        nums2: The second sorted list of integers.

    Returns:
        The median of the combined sorted arrays as a float.
    """
    m, n = len(nums1), len(nums2)

    # Ensure nums1 is the shorter array for O(log(min(m,n))) complexity
    if m > n:
        nums1, nums2 = nums2, nums1
        m, n = n, m

    low, high = 0, m
    # half_len represents the target number of elements in the left partition
    # of the combined sorted array. The +1 handles both odd and even total lengths.
    half_len = (m + n + 1) // 2

    while low <= high:
        cut1 = (low + high) // 2  # Partition point for nums1
        cut2 = half_len - cut1    # Partition point for nums2

        # Determine elements around the cuts.
        # Use -float('inf') and float('inf') for boundary conditions
        # when a cut is at the very beginning (0) or very end (m/n).
        L1 = float('-inf') if cut1 == 0 else nums1[cut1 - 1]
        R1 = float('inf') if cut1 == m else nums1[cut1]

        L2 = float('-inf') if cut2 == 0 else nums2[cut2 - 1]
        R2 = float('inf') if cut2 == n else nums2[cut2]

        if L1 <= R2 and L2 <= R1:
            # Correct partition found.
            # All elements in the left halves (L1, L2) are <= elements in the right halves (R1, R2).
            if (m + n) % 2 == 1:
                # Total length is odd, median is the largest element in the left half.
                return float(max(L1, L2))
            else:
                # Total length is even, median is the average of the two middle elements.
                return (max(L1, L2) + min(R1, R2)) / 2.0
        elif L1 > R2:
            # cut1 is too far right (L1 is too large). Need to move cut1 to the left.
            high = cut1 - 1
        else:  # L2 > R1
            # cut1 is too far left (L2 is too large). Need to move cut1 to the right.
            low = cut1 + 1
    
    # This line should theoretically not be reached with valid inputs and a correct algorithm,
    # as a solution must always be found within the binary search range.
    return 0.0 # Placeholder for unreachable code path

def main():
    """
    Reads two lines of comma-separated integers from stdin,
    finds the median of the combined sorted arrays, and prints it.
    """
    line1 = sys.stdin.readline().strip()
    line2 = sys.stdin.readline().strip()

    # Parse lines, filtering out potential empty strings from split if present
    nums1_str = [x for x in line1.split(',') if x.strip()]
    nums2_str = [x for x in line2.split(',') if x.strip()]
    
    nums1 = [int(x) for x in nums1_str]
    nums2 = [int(x) for x in nums2_str]
    
    median = find_median_sorted_arrays(nums1, nums2)
    print(median)

if __name__ == "__main__":
    main()
