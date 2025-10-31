"""
CodeSmith CLI - Main entrypoint for running tasks.
"""

import sys
import argparse
import json
from pathlib import Path

from .agent import CodeSmithAgent
from .sandbox import CodeSandbox
from .orchestrator import TaskOrchestrator
from .tasks import get_task, list_tasks


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="CodeSmith - Autonomous Python Code Generation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'task',
        nargs='?',
        help='Task name or path to task JSON file'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available example tasks'
    )
    
    parser.add_argument(
        '--llm',
        choices=['mock', 'openai', 'anthropic', 'gemini'],
        default='mock',
        help='LLM provider to use (default: mock)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key for LLM provider (or set via env var)'
    )
    
    parser.add_argument(
        '--max-attempts',
        type=int,
        default=3,
        help='Maximum repair attempts (default: 3)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        help='Save final code to file'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # List tasks
    if args.list:
        print("Available example tasks:")
        for task_name in list_tasks():
            print(f"  - {task_name}")
        return 0
    
    # Load task
    if not args.task:
        parser.print_help()
        return 1
    
    try:
        # Try loading as example task first
        try:
            task_spec = get_task(args.task)
            print(f"Running example task: {args.task}")
        except ValueError:
            # Try loading as JSON file
            with open(args.task, 'r') as f:
                task_spec = json.load(f)
            print(f"Running task from file: {args.task}")
    
    except Exception as e:
        print(f"Error loading task: {e}", file=sys.stderr)
        return 1
    
    # Initialize components
    print(f"\nInitializing CodeSmith with {args.llm} provider...")
    agent = CodeSmithAgent(llm_provider=args.llm, api_key=args.api_key)
    sandbox = CodeSandbox()
    orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=args.max_attempts)
    
    # Run task
    print(f"\nTask: {task_spec['task'][:100]}...")
    result = orchestrator.run_task(task_spec)
    
    # Display results
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Success: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    
    if result['success'] and result['final_code']:
        print(f"\nFinal code ({len(result['final_code'])} chars):")
        print("-" * 60)
        print(result['final_code'])
        print("-" * 60)
        
        # Save to file if requested
        if args.output:
            args.output.write_text(result['final_code'])
            print(f"\n✅ Code saved to: {args.output}")
    
    # Verbose history
    if args.verbose:
        print("\n" + "="*60)
        print("ATTEMPT HISTORY")
        print("="*60)
        for record in result['history']:
            print(f"\nAttempt {record['attempt']}:")
            print(f"  Plan: {record.get('plan', 'N/A')[:80]}...")
            if 'doctest_result' in record and record['doctest_result']:
                dr = record['doctest_result']
                print(f"  Doctests: {dr['passed']} passed, {dr['failed']} failed")
            if 'test_result' in record and record['test_result']:
                tr = record['test_result']
                print(f"  Tests: {tr['passed']} passed, {tr['failed']} failed")
            print(f"  Success: {record.get('success', False)}")
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
