"""
Comprehensive CodeSmith Demo with Gemini API - All 5 Example Tasks
Tests: sum, fibonacci, palindrome, prime, reverse_words
"""

from codesmith.agent import CodeSmithAgent
from codesmith.sandbox import CodeSandbox
from codesmith.orchestrator import TaskOrchestrator

# Your Gemini API key
API_KEY = "AIzaSyDTocyWrmsKwqna1JaWIreHKAaOvubvRNk"

def print_header(title: str, char: str = "="):
    print(f"\n{char * 70}")
    print(title)
    print(f"{char * 70}\n")

def run_task(task_name: str, task_desc: str, test_cases: list, run_doctests: bool = False):
    """Run a single task with Gemini."""
    print_header(f"Task: {task_name}", "=")
    
    agent = CodeSmithAgent(llm_provider='gemini', api_key=API_KEY)
    sandbox = CodeSandbox()
    orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=3)
    
    task_spec = {
        "task": task_desc,
        "test_cases": test_cases,
        "run_doctests": run_doctests
    }
    
    result = orchestrator.run_task(task_spec)
    
    if result['success']:
        print(f"\n✅ {task_name} completed in {result['attempts']} attempts")
        return True
    else:
        print(f"\n❌ {task_name} FAILED after {result['attempts']} attempts")
        print(f"Final error: {result.get('final_error', 'Unknown')}")
        return False

def main():
    print_header("CodeSmith Demo - All 5 Example Tasks with Gemini API", "=")
    
    tasks = [
        {
            "name": "Sum Two Numbers",
            "desc": "Write a Python program that reads two integers from stdin (using sys.stdin.readline() twice) and prints their sum. No command-line arguments, no doctests.",
            "tests": [
                {"input": "5\n3", "expected": "8"},
                {"input": "10\n-2", "expected": "8"}
            ],
            "doctests": False
        },
        {
            "name": "Fibonacci",
            "desc": "Write a Python program that reads an integer N from stdin (using sys.stdin.readline()) and prints the first N Fibonacci numbers separated by spaces. No command-line arguments, no doctests.",
            "tests": [
                {"input": "5", "expected": "0 1 1 2 3"},
                {"input": "7", "expected": "0 1 1 2 3 5 8"}
            ],
            "doctests": False
        },
        {
            "name": "Palindrome",
            "desc": "Write a Python program that reads a string from stdin (using sys.stdin.readline()) and prints 'true' if it's a palindrome (ignoring case and spaces), 'false' otherwise. No command-line arguments, no doctests.",
            "tests": [
                {"input": "racecar", "expected": "true"},
                {"input": "A man a plan a canal Panama", "expected": "true"}
            ],
            "doctests": False
        },
        {
            "name": "Prime Checker",
            "desc": "Write a Python program that reads an integer N from stdin (using sys.stdin.readline()) and prints 'prime' if N is prime, 'not prime' otherwise. Handle edge cases where N < 2 (not prime). No command-line arguments, no doctests.",
            "tests": [
                {"input": "2", "expected": "prime"},
                {"input": "17", "expected": "prime"},
                {"input": "4", "expected": "not prime"},
                {"input": "97", "expected": "prime"}
            ],
            "doctests": False
        },
        {
            "name": "Reverse Words",
            "desc": "Write a Python program that reads a sentence from stdin (using sys.stdin.readline()) and prints the sentence with words in reverse order. Preserve spaces between words. No command-line arguments, no doctests.",
            "tests": [
                {"input": "hello world", "expected": "world hello"},
                {"input": "Python is great", "expected": "great is Python"}
            ],
            "doctests": False
        }
    ]
    
    results = {}
    for task in tasks:
        success = run_task(
            task_name=task["name"],
            task_desc=task["desc"],
            test_cases=task["tests"],
            run_doctests=task["doctests"]
        )
        results[task["name"]] = success
    
    # Print summary
    print_header("SUMMARY", "=")
    passed = sum(results.values())
    total = len(results)
    
    for task_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{task_name:30} {status}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! CodeSmith with Gemini is fully functional.")
    else:
        print(f"\n⚠️  {total - passed} task(s) failed. Review logs above.")

if __name__ == "__main__":
    main()
