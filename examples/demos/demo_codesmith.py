"""
Demo script to show CodeSmith in action.
"""

from codesmith.agent import CodeSmithAgent
from codesmith.sandbox import CodeSandbox
from codesmith.orchestrator import TaskOrchestrator


def demo_simple_task():
    """Demo with a simple task that should pass on first attempt."""
    print("="*70)
    print("DEMO: Simple Mean Calculation Task")
    print("="*70)
    
    task_spec = {
        "task": "Write a CLI that reads CSV integers and prints their mean to 2 decimals",
        "test_cases": [
            {"input": "1,2,3,4,5", "expected": "3.0"},
            {"input": "10,20,30", "expected": "20.0"},
        ],
        "run_doctests": False  # Disable doctests for simplicity
    }
    
    agent = CodeSmithAgent(llm_provider='mock')
    sandbox = CodeSandbox()
    orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=3)
    
    result = orchestrator.run_task(task_spec)
    
    print("\n" + "="*70)
    print(f"✅ SUCCESS: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    if result['final_code']:
        print("\nGenerated Code:")
        print("-"*70)
        print(result['final_code'])
        print("-"*70)
    
    return result


def demo_fibonacci():
    """Demo Fibonacci task."""
    print("\n" + "="*70)
    print("DEMO: Fibonacci Task")
    print("="*70)
    
    task_spec = {
        "task": "Write a CLI that reads N and prints first N Fibonacci numbers",
        "test_cases": [
            {"input": "5", "expected": "0 1 1 2 3"},
            {"input": "1", "expected": "0"},
            {"input": "7", "expected": "0 1 1 2 3 5 8"},
        ],
        "run_doctests": False
    }
    
    agent = CodeSmithAgent(llm_provider='mock')
    sandbox = CodeSandbox()
    orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=3)
    
    result = orchestrator.run_task(task_spec)
    
    print("\n" + "="*70)
    print(f"✅ SUCCESS: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    
    return result


def demo_palindrome():
    """Demo palindrome checker."""
    print("\n" + "="*70)
    print("DEMO: Palindrome Checker")
    print("="*70)
    
    task_spec = {
        "task": "Write a CLI that checks if input is palindrome (print 'true' or 'false')",
        "test_cases": [
            {"input": "racecar", "expected": "true"},
            {"input": "hello", "expected": "false"},
            {"input": "A man a plan a canal Panama", "expected": "true"},
        ],
        "run_doctests": False
    }
    
    agent = CodeSmithAgent(llm_provider='mock')
    sandbox = CodeSandbox()
    orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=3)
    
    result = orchestrator.run_task(task_spec)
    
    print("\n" + "="*70)
    print(f"✅ SUCCESS: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    
    return result


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "CodeSmith Demo Suite" + " "*28 + "║")
    print("╚" + "="*68 + "╝")
    
    results = []
    
    # Run demos
    results.append(("Mean", demo_simple_task()))
    results.append(("Fibonacci", demo_fibonacci()))
    results.append(("Palindrome", demo_palindrome()))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for name, result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{name:20} {status:10} ({result['attempts']} attempts)")
    
    total_pass = sum(1 for _, r in results if r['success'])
    print(f"\nTotal: {total_pass}/{len(results)} passed")


if __name__ == '__main__':
    main()
