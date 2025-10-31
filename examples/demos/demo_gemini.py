"""
Demo CodeSmith with Gemini API.
"""

from codesmith.agent import CodeSmithAgent
from codesmith.sandbox import CodeSandbox
from codesmith.orchestrator import TaskOrchestrator

API_KEY = "AIzaSyDTocyWrmsKwqna1JaWIreHKAaOvubvRNk"

def demo_gemini():
    """Demo with Gemini API."""
    print("="*70)
    print("CodeSmith Demo with Gemini API")
    print("="*70)
    
    tasks = [
        {
            "name": "Sum Two Numbers",
            "spec": {
                "task": "Write a CLI that reads two integers from separate stdin lines and prints their sum. Use sys.stdin.readline(). No doctests.",
                "test_cases": [
                    {"input": "5\n3", "expected": "8"},
                    {"input": "10\n20", "expected": "30"},
                ],
                "run_doctests": False
            }
        },
        {
            "name": "Fibonacci",
            "spec": {
                "task": "Write a CLI that reads N from stdin and prints first N Fibonacci numbers space-separated. Use sys.stdin.readline(). No doctests.",
                "test_cases": [
                    {"input": "5", "expected": "0 1 1 2 3"},
                    {"input": "1", "expected": "0"},
                ],
                "run_doctests": False
            }
        },
        {
            "name": "Palindrome",
            "spec": {
                "task": "Write a CLI that reads a string from stdin and prints 'true' if palindrome, 'false' otherwise. Ignore case/spaces. Use sys.stdin.readline(). No doctests.",
                "test_cases": [
                    {"input": "racecar", "expected": "true"},
                    {"input": "hello", "expected": "false"},
                ],
                "run_doctests": False
            }
        }
    ]
    
    results = []
    
    for task_info in tasks:
        print(f"\n{'='*70}")
        print(f"Task: {task_info['name']}")
        print(f"{'='*70}")
        
        agent = CodeSmithAgent(llm_provider='gemini', api_key=API_KEY)
        sandbox = CodeSandbox()
        orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=3)
        
        result = orchestrator.run_task(task_info['spec'])
        
        results.append({
            'name': task_info['name'],
            'success': result['success'],
            'attempts': result['attempts']
        })
        
        if result['success']:
            print(f"\n✅ {task_info['name']} completed in {result['attempts']} attempts")
        else:
            print(f"\n❌ {task_info['name']} failed after {result['attempts']} attempts")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for r in results:
        status = "✅ PASS" if r['success'] else "❌ FAIL"
        print(f"{r['name']:30} {status:10} ({r['attempts']} attempts)")
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    print(f"\nTotal: {passed}/{total} passed")
    
    return passed == total


if __name__ == '__main__':
    import sys
    success = demo_gemini()
    sys.exit(0 if success else 1)
