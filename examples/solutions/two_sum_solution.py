import sys

def main():
    """
    Reads two lines from stdin to find two indices where numbers add up to a target.
    First line: comma-separated integers (the array).
    Second line: target integer.
    Prints the two indices space-separated (e.g., '0 1').
    Each input has exactly one solution.
    """
    # Read the first line from stdin, remove leading/trailing whitespace, and parse integers
    line1 = sys.stdin.readline().strip()
    nums = [int(x) for x in line1.split(',')]

    # Read the second line from stdin, remove whitespace, and parse the target integer
    line2 = sys.stdin.readline().strip()
    target = int(line2)

    # Dictionary to store number -> index mappings for O(1) lookups
    num_map = {}

    # Iterate through the array with indices
    for i, num in enumerate(nums):
        complement = target - num

        # Check if the complement is already in our map
        if complement in num_map:
            # If found, print the stored index for the complement and the current index
            print(f"{num_map[complement]} {i}")
            return # Exit after finding the unique solution
        
        # If complement not found, add the current number and its index to the map
        num_map[num] = i

if __name__ == "__main__":
    main()
