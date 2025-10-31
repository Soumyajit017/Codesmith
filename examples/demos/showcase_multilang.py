"""
CodeSmith Multi-Language Showcase
==================================
Demonstrates the complete workflow: LeetCode → Multi-Language Solutions

This demo shows:
1. Parsing a LeetCode problem
2. Generating solutions in Python, C++, Java, JavaScript
3. Displaying algorithm and complexity analysis
4. Saving all solutions
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from codesmith.leetcode_parser import LeetCodeParser
from codesmith.multilang import MultiLanguageGenerator


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text):
    """Print a section divider."""
    print("\n" + "-" * 80)
    print(f"  {text}")
    print("-" * 80)


def showcase_leetcode_parsing():
    """Demonstrate LeetCode problem parsing."""
    print_header("STEP 1: Parse LeetCode Problem")
    
    # Sample LeetCode problem
    problem_text = """
Two Sum

Given an array of integers nums and an integer target, return indices of the 
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may 
not use the same element twice.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- Only one valid answer exists.

Time Complexity: O(n)
Space Complexity: O(n)
"""
    
    parser = LeetCodeParser()
    parsed = parser.parse_leetcode_problem(problem_text)
    
    print(f"\n✅ Successfully parsed problem!")
    print(f"   Title: {parsed['title']}")
    print(f"   Difficulty: {parsed['difficulty']}")
    print(f"   Examples: {len(parsed['examples'])}")
    print(f"   Constraints: {len(parsed['constraints'])}")
    
    # Convert to task formats
    print_section("Converting to Task Specifications")
    
    tasks = {}
    for lang in ['python', 'cpp', 'java', 'javascript']:
        task = parser.convert_to_codesmith_format(parsed, lang)
        tasks[lang] = task
        print(f"   ✅ {lang.upper()}: {len(task['test_cases'])} test cases")
    
    return tasks['python']  # Return Python task for demo


def showcase_multilang_generation(task_spec):
    """Demonstrate multi-language code generation."""
    print_header("STEP 2: Generate Multi-Language Solutions")
    
    # Note: Using mock provider for demo (no API key needed)
    generator = MultiLanguageGenerator(llm_provider='mock')
    
    print("\n📝 Task: Two Sum")
    print("🤖 LLM Provider: Mock (for demonstration)")
    print("🌍 Languages: Python, C++, Java, JavaScript\n")
    
    # Generate code
    results = generator.generate_all_languages(task_spec, max_attempts=1)
    
    # Display results
    print_section("Results Summary")
    generator.print_results_table()
    
    return results


def showcase_solution_details(results):
    """Show details of generated solutions."""
    print_header("STEP 3: Solution Details")
    
    for lang, result in results.items():
        print_section(f"{lang.upper()} Solution")
        
        if result.success:
            print(f"✅ Status: Successfully generated")
            print(f"⏱️  Generation time: {result.time_taken:.2f}s")
            print(f"🔄 Attempts needed: {result.attempts}")
            print(f"🧮 Algorithm: {result.algorithm}")
            print(f"⏰ Time complexity: {result.time_complexity}")
            print(f"💾 Space complexity: {result.space_complexity}")
            
            # Show code preview
            print(f"\n📝 Code Preview (first 15 lines):")
            code_lines = result.code.split('\n')
            lines = code_lines[:15]
            for i, line in enumerate(lines, 1):
                print(f"    {i:2d} | {line}")
            if len(code_lines) > 15:
                remaining = len(code_lines) - 15
                print(f"    ... ({remaining} more lines)")
        else:
            print(f"❌ Status: Failed")
            print(f"❌ Error: {result.error}")


def showcase_file_output(results):
    """Demonstrate file saving."""
    print_header("STEP 4: Save Solutions")
    
    # Create demo output directory
    output_dir = 'showcase_output'
    os.makedirs(output_dir, exist_ok=True)
    
    generator = MultiLanguageGenerator(llm_provider='mock')
    generator.results = results
    generator.save_results(output_dir)
    
    print(f"\n✅ All solutions saved to: {output_dir}/\n")
    
    # List generated files
    for lang in ['python', 'cpp', 'java', 'javascript']:
        ext = {'python': 'py', 'cpp': 'cpp', 'java': 'java', 'javascript': 'js'}[lang]
        filepath = os.path.join(output_dir, f'solution.{ext}')
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   📄 solution.{ext:<4} ({size:,} bytes)")


def main():
    """Run the complete showcase."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "CODESMITH MULTI-LANGUAGE SHOWCASE" + " " * 25 + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Demonstrates:" + " " * 63 + "║")
    print("║" + "    • LeetCode problem parsing" + " " * 48 + "║")
    print("║" + "    • Multi-language code generation (Python, C++, Java, JS)" + " " * 16 + "║")
    print("║" + "    • Algorithm and complexity detection" + " " * 39 + "║")
    print("║" + "    • Structured results display" + " " * 47 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Step 1: Parse LeetCode problem
        task_spec = showcase_leetcode_parsing()
        
        # Step 2: Generate multi-language solutions
        results = showcase_multilang_generation(task_spec)
        
        # Step 3: Show solution details
        showcase_solution_details(results)
        
        # Step 4: Save files
        showcase_file_output(results)
        
        # Final summary
        print_header("🎉 SHOWCASE COMPLETE!")
        
        success_count = sum(1 for r in results.values() if r.success)
        print(f"\n✅ Successfully generated {success_count}/{len(results)} language solutions")
        print(f"📁 All files saved to: showcase_output/")
        print(f"\n💡 Next Steps:")
        print(f"   1. Check showcase_output/ for generated code")
        print(f"   2. Try with a real LLM: run_multilang.py full problem.txt --llm gemini --api-key KEY")
        print(f"   3. Read docs/MULTILANG_GUIDE.md for full usage guide")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
