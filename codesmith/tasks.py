"""
Example task specifications for testing CodeSmith.
"""

EXAMPLE_TASKS = {
    "fibonacci": {
        "task": """Write a CLI program that reads an integer N from stdin and prints the first N Fibonacci numbers separated by spaces.
Include doctests and proper input validation.""",
        "test_cases": [
            {"input": "5", "expected": "0 1 1 2 3"},
            {"input": "1", "expected": "0"},
            {"input": "7", "expected": "0 1 1 2 3 5 8"},
            {"input": "0", "expected": ""}
        ],
        "run_doctests": True
    },
    
    "mean": {
        "task": """Write a CLI program that reads a CSV line of integers and prints their mean rounded to 2 decimals.
Include doctests and proper input validation.""",
        "test_cases": [
            {"input": "1,2,3,4,5", "expected": "3.0"},
            {"input": "10,20,30", "expected": "20.0"},
            {"input": "7", "expected": "7.0"},
            {"input": "100,200", "expected": "150.0"}
        ],
        "run_doctests": True
    },
    
    "palindrome": {
        "task": """Write a CLI program that reads a string and prints 'true' if it's a palindrome, 'false' otherwise.
Ignore case, spaces, and punctuation. Include doctests.""",
        "test_cases": [
            {"input": "racecar", "expected": "true"},
            {"input": "hello", "expected": "false"},
            {"input": "A man a plan a canal Panama", "expected": "true"},
            {"input": "Was it a car or a cat I saw", "expected": "true"},
            {"input": "", "expected": "true"}
        ],
        "run_doctests": True
    },
    
    "prime": {
        "task": """Write a CLI program that reads an integer N and prints 'prime' if N is prime, 'not prime' otherwise.
Include doctests and handle edge cases (N < 2).""",
        "test_cases": [
            {"input": "2", "expected": "prime"},
            {"input": "17", "expected": "prime"},
            {"input": "4", "expected": "not prime"},
            {"input": "1", "expected": "not prime"},
            {"input": "97", "expected": "prime"}
        ],
        "run_doctests": True
    },
    
    "reverse_words": {
        "task": """Write a CLI program that reads a sentence and prints it with words in reverse order.
Preserve original spacing. Include doctests.""",
        "test_cases": [
            {"input": "hello world", "expected": "world hello"},
            {"input": "Python is great", "expected": "great is Python"},
            {"input": "a", "expected": "a"},
            {"input": "one two three four", "expected": "four three two one"}
        ],
        "run_doctests": True
    }
}


def get_task(name: str):
    """Get a task specification by name."""
    if name not in EXAMPLE_TASKS:
        raise ValueError(f"Unknown task: {name}. Available: {list(EXAMPLE_TASKS.keys())}")
    return EXAMPLE_TASKS[name]


def list_tasks():
    """List all available example tasks."""
    return list(EXAMPLE_TASKS.keys())
