#!/usr/bin/env python3
"""
CodeSmith Multi-Language CLI
Parse LeetCode problems and generate solutions in multiple languages.
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from codesmith.leetcode_parser import LeetCodeParser
from codesmith.multilang import MultiLanguageGenerator


def parse_leetcode_command(args):
    """Parse LeetCode problem and save to JSON."""
    parser = LeetCodeParser()
    
    # Read problem text
    if args.input == '-':
        print("Paste LeetCode problem text (Ctrl+D or Ctrl+Z when done):")
        problem_text = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            problem_text = f.read()
    
    # Parse
    print("\n🔍 Parsing LeetCode problem...")
    parsed = parser.parse_leetcode_problem(problem_text)
    
    print(f"\n✅ Parsed: {parsed['title']}")
    print(f"   Difficulty: {parsed['difficulty']}")
    print(f"   Time Complexity: {parsed['time_complexity']}")
    print(f"   Space Complexity: {parsed['space_complexity']}")
    print(f"   Examples: {len(parsed['examples'])}")
    print(f"   Constraints: {len(parsed['constraints'])}")
    
    # Convert to task format for each language
    languages = args.languages or ['python', 'cpp', 'java', 'javascript']
    
    output_dir = args.output_dir or 'tasks'
    os.makedirs(output_dir, exist_ok=True)
    
    title_slug = parsed['title'].lower().replace(' ', '_').replace('-', '_')
    
    for lang in languages:
        task_spec = parser.convert_to_codesmith_format(parsed, lang)
        output_file = os.path.join(output_dir, f"{title_slug}_{lang}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(task_spec, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ {lang.upper()}: {output_file}")
    
    print(f"\n📁 Task files saved to: {output_dir}/")
    return title_slug, languages


def generate_multilang_command(args):
    """Generate code in multiple languages."""
    # Load task file
    with open(args.task_file, 'r', encoding='utf-8') as f:
        task_spec = json.load(f)
    
    print(f"\n🚀 Generating code for: {task_spec.get('metadata', {}).get('title', 'Task')}")
    print(f"   LLM Provider: {args.llm}")
    print(f"   Languages: {', '.join(args.languages or ['all'])}")
    
    # Create generator
    generator = MultiLanguageGenerator(
        llm_provider=args.llm,
        api_key=args.api_key
    )
    
    # Filter languages if specified
    if args.languages:
        generator.SUPPORTED_LANGUAGES = [
            l for l in args.languages 
            if l in generator.SUPPORTED_LANGUAGES
        ]
    
    # Generate
    results = generator.generate_all_languages(task_spec, max_attempts=args.max_attempts)
    
    # Display results
    generator.print_results_table()
    
    # Save
    output_dir = args.output_dir or 'solutions'
    generator.save_results(output_dir)
    
    return results


def full_workflow_command(args):
    """Full workflow: parse LeetCode -> generate all languages."""
    print("\n" + "="*70)
    print("CODESMITH MULTI-LANGUAGE WORKFLOW")
    print("="*70)
    
    # Step 1: Parse LeetCode problem
    print("\n📝 STEP 1: Parsing LeetCode Problem")
    print("-"*70)
    
    parse_args = argparse.Namespace(
        input=args.input,
        output_dir='tasks',
        languages=args.languages
    )
    title_slug, languages = parse_leetcode_command(parse_args)
    
    # Step 2: Generate code for each language
    print("\n💻 STEP 2: Generating Multi-Language Solutions")
    print("-"*70)
    
    # Use Python task as base (it has the most complete info)
    python_task_file = f"tasks/{title_slug}_python.json"
    
    gen_args = argparse.Namespace(
        task_file=python_task_file,
        llm=args.llm,
        api_key=args.api_key,
        output_dir=f'solutions/{title_slug}',
        languages=args.languages,
        max_attempts=args.max_attempts
    )
    
    results = generate_multilang_command(gen_args)
    
    # Summary
    print("\n" + "="*70)
    print("🎉 WORKFLOW COMPLETE!")
    print("="*70)
    print(f"\n📁 Task JSONs: tasks/{title_slug}_*.json")
    print(f"📁 Solutions: solutions/{title_slug}/")
    
    success_count = sum(1 for r in results.values() if r.success)
    print(f"\n✅ Successfully generated {success_count}/{len(results)} language solutions")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CodeSmith Multi-Language Code Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Parse LeetCode problem
  python run_multilang.py parse problem.txt
  
  # Generate from existing task
  python run_multilang.py generate task.json --llm gemini --api-key KEY
  
  # Full workflow
  python run_multilang.py full problem.txt --llm gemini --api-key KEY
  
  # Parse from clipboard (paste and Ctrl+D)
  python run_multilang.py parse -
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse LeetCode problem to JSON')
    parse_parser.add_argument('input', help='Problem text file (or - for stdin)')
    parse_parser.add_argument('--output-dir', default='tasks', help='Output directory')
    parse_parser.add_argument('--languages', nargs='+', 
                             choices=['python', 'cpp', 'java', 'javascript'],
                             help='Languages to generate tasks for')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate multi-language code')
    gen_parser.add_argument('task_file', help='Task JSON file')
    gen_parser.add_argument('--llm', default='gemini', help='LLM provider')
    gen_parser.add_argument('--api-key', help='API key for LLM')
    gen_parser.add_argument('--output-dir', help='Output directory')
    gen_parser.add_argument('--languages', nargs='+',
                           choices=['python', 'cpp', 'java', 'javascript'],
                           help='Languages to generate')
    gen_parser.add_argument('--max-attempts', type=int, default=3, 
                           help='Max repair attempts')
    
    # Full workflow command
    full_parser = subparsers.add_parser('full', help='Full workflow (parse + generate)')
    full_parser.add_argument('input', help='Problem text file (or - for stdin)')
    full_parser.add_argument('--llm', default='gemini', help='LLM provider')
    full_parser.add_argument('--api-key', help='API key for LLM')
    full_parser.add_argument('--languages', nargs='+',
                            choices=['python', 'cpp', 'java', 'javascript'],
                            help='Languages to generate')
    full_parser.add_argument('--max-attempts', type=int, default=3,
                            help='Max repair attempts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    try:
        if args.command == 'parse':
            parse_leetcode_command(args)
        elif args.command == 'generate':
            generate_multilang_command(args)
        elif args.command == 'full':
            full_workflow_command(args)
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
