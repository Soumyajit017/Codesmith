"""
LeetCode Problem Parser
Converts LeetCode problem descriptions to CodeSmith task format.
"""

import json
import re
from typing import Dict, List, Any


class LeetCodeParser:
    """Parse LeetCode problems and convert to CodeSmith format."""
    
    def __init__(self):
        self.language_mappings = {
            'python': self._convert_to_python_format,
            'cpp': self._convert_to_cpp_format,
            'java': self._convert_to_java_format,
            'javascript': self._convert_to_js_format
        }
    
    def parse_leetcode_problem(self, problem_text: str) -> Dict[str, Any]:
        """
        Parse LeetCode problem text and extract structured information.
        
        Args:
            problem_text: Raw LeetCode problem description
            
        Returns:
            Structured task specification for CodeSmith
        """
        # Extract title
        title = self._extract_title(problem_text)
        
        # Extract difficulty
        difficulty = self._extract_difficulty(problem_text)
        
        # Extract description
        description = self._extract_description(problem_text)
        
        # Extract examples
        examples = self._extract_examples(problem_text)
        
        # Extract constraints
        constraints = self._extract_constraints(problem_text)
        
        # Extract complexity requirements
        time_complexity, space_complexity = self._extract_complexity(problem_text)
        
        # Generate test cases from examples
        test_cases = self._generate_test_cases(examples)
        
        return {
            'title': title,
            'difficulty': difficulty,
            'description': description,
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'examples': examples,
            'constraints': constraints,
            'test_cases': test_cases
        }
    
    def convert_to_codesmith_format(self, parsed_problem: Dict[str, Any], 
                                   language: str = 'python') -> Dict[str, Any]:
        """
        Convert parsed LeetCode problem to CodeSmith task format.
        
        Args:
            parsed_problem: Parsed problem dictionary
            language: Target programming language
            
        Returns:
            CodeSmith-compatible task specification
        """
        converter = self.language_mappings.get(language, self._convert_to_python_format)
        return converter(parsed_problem)
    
    def _extract_title(self, text: str) -> str:
        """Extract problem title."""
        # Look for patterns like "1. Two Sum" or "Median of Two Sorted Arrays"
        title_match = re.search(r'^\d+\.\s*(.+?)(?:\n|$)', text, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Try first line
        first_line = text.split('\n')[0].strip()
        return first_line if first_line else "Untitled Problem"
    
    def _extract_difficulty(self, text: str) -> str:
        """Extract difficulty level."""
        text_lower = text.lower()
        if 'easy' in text_lower:
            return 'Easy'
        elif 'medium' in text_lower:
            return 'Medium'
        elif 'hard' in text_lower:
            return 'Hard'
        return 'Medium'  # Default
    
    def _extract_description(self, text: str) -> str:
        """Extract problem description."""
        # Remove examples and constraints sections
        desc = re.split(r'Example\s*\d*:', text, flags=re.IGNORECASE)[0]
        desc = re.split(r'Constraints?:', desc, flags=re.IGNORECASE)[0]
        
        # Clean up
        desc = re.sub(r'^\d+\.\s*.*?\n', '', desc)  # Remove title line
        desc = re.sub(r'(Easy|Medium|Hard)\s*\n', '', desc, flags=re.IGNORECASE)
        
        return desc.strip()
    
    def _extract_examples(self, text: str) -> List[Dict[str, Any]]:
        """Extract example inputs and outputs."""
        examples = []
        
        # Find all example blocks
        example_pattern = r'Example\s*(\d+):(.*?)(?=Example\s*\d+:|Constraints?:|$)'
        matches = re.finditer(example_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            example_text = match.group(2)
            
            # Extract input
            input_match = re.search(r'Input:\s*(.+?)(?:\n|Output:|$)', example_text, re.DOTALL)
            # Extract output
            output_match = re.search(r'Output:\s*(.+?)(?:\n|Explanation:|$)', example_text, re.DOTALL)
            # Extract explanation
            explanation_match = re.search(r'Explanation:\s*(.+?)(?:\n\n|$)', example_text, re.DOTALL)
            
            if input_match and output_match:
                examples.append({
                    'input': input_match.group(1).strip(),
                    'output': output_match.group(1).strip(),
                    'explanation': explanation_match.group(1).strip() if explanation_match else ''
                })
        
        return examples
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract problem constraints."""
        constraints = []
        
        # Find constraints section
        constraints_match = re.search(r'Constraints?:(.*?)(?=\n\n|$)', text, re.IGNORECASE | re.DOTALL)
        
        if constraints_match:
            constraints_text = constraints_match.group(1)
            # Split by newlines and bullet points
            lines = constraints_text.split('\n')
            for line in lines:
                line = line.strip()
                # Remove bullets
                line = re.sub(r'^[-*•]\s*', '', line)
                if line:
                    constraints.append(line)
        
        return constraints
    
    def _extract_complexity(self, text: str) -> tuple:
        """Extract time and space complexity requirements."""
        time_complexity = "Not specified"
        space_complexity = "Not specified"
        
        # Look for complexity mentions
        time_match = re.search(r'O\([^)]+\)\s*time', text, re.IGNORECASE)
        if time_match:
            time_complexity = time_match.group(0)
        
        space_match = re.search(r'O\([^)]+\)\s*space', text, re.IGNORECASE)
        if space_match:
            space_complexity = space_match.group(0)
        
        return time_complexity, space_complexity
    
    def _generate_test_cases(self, examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate test cases from examples."""
        test_cases = []
        
        for example in examples:
            # Parse input and output
            input_str = self._parse_leetcode_input(example['input'])
            output_str = self._parse_leetcode_output(example['output'])
            
            test_cases.append({
                'input': input_str,
                'expected': output_str
            })
        
        return test_cases
    
    def _parse_leetcode_input(self, input_str: str) -> str:
        """Convert LeetCode input format to stdin format."""
        # Example: "nums = [2,7,11,15], target = 9" -> "2,7,11,15\n9"
        
        # Extract array/list values
        arrays = re.findall(r'\[([^\]]+)\]', input_str)
        # Extract scalar values
        scalars = re.findall(r'=\s*(-?\d+(?:\.\d+)?)\s*(?:,|$)', input_str)
        
        result_parts = []
        
        # Add arrays (comma-separated)
        for arr in arrays:
            result_parts.append(arr.replace(' ', ''))
        
        # Add scalars not in arrays
        if scalars:
            # Filter out values that are already in arrays
            for scalar in scalars:
                if scalar not in ' '.join(arrays):
                    result_parts.append(scalar)
        
        return '\n'.join(result_parts)
    
    def _parse_leetcode_output(self, output_str: str) -> str:
        """Convert LeetCode output format to stdout format."""
        # Example: "[0,1]" -> "0 1"
        # Example: "2" -> "2"
        # Example: "true" -> "true"
        
        output_str = output_str.strip()
        
        # Handle arrays
        if output_str.startswith('[') and output_str.endswith(']'):
            # Extract array contents
            content = output_str[1:-1]
            # Convert to space-separated
            return content.replace(',', ' ').replace(' ', ' ')
        
        # Handle booleans
        if output_str.lower() in ['true', 'false']:
            return output_str.lower()
        
        # Handle numbers and strings
        return output_str
    
    def _convert_to_python_format(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to Python task format."""
        return {
            'language': 'python',
            'task': f"Write a Python program that reads input from stdin (using sys.stdin.readline()) and solves: {parsed['description']}. No command-line arguments, no doctests.",
            'test_cases': parsed['test_cases'],
            'run_doctests': False,
            'metadata': {
                'title': parsed['title'],
                'difficulty': parsed['difficulty'],
                'time_complexity': parsed['time_complexity'],
                'space_complexity': parsed['space_complexity'],
                'constraints': parsed['constraints']
            }
        }
    
    def _convert_to_cpp_format(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to C++ task format."""
        return {
            'language': 'cpp',
            'task': f"Write a C++ program that reads input from stdin and solves: {parsed['description']}. Use efficient algorithms.",
            'test_cases': parsed['test_cases'],
            'run_doctests': False,
            'metadata': {
                'title': parsed['title'],
                'difficulty': parsed['difficulty'],
                'time_complexity': parsed['time_complexity'],
                'space_complexity': parsed['space_complexity'],
                'constraints': parsed['constraints']
            }
        }
    
    def _convert_to_java_format(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to Java task format."""
        return {
            'language': 'java',
            'task': f"Write a Java program that reads input from stdin and solves: {parsed['description']}. Use Scanner for input.",
            'test_cases': parsed['test_cases'],
            'run_doctests': False,
            'metadata': {
                'title': parsed['title'],
                'difficulty': parsed['difficulty'],
                'time_complexity': parsed['time_complexity'],
                'space_complexity': parsed['space_complexity'],
                'constraints': parsed['constraints']
            }
        }
    
    def _convert_to_js_format(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to JavaScript task format."""
        return {
            'language': 'javascript',
            'task': f"Write a JavaScript program that reads input from stdin and solves: {parsed['description']}. Use readline or process.stdin.",
            'test_cases': parsed['test_cases'],
            'run_doctests': False,
            'metadata': {
                'title': parsed['title'],
                'difficulty': parsed['difficulty'],
                'time_complexity': parsed['time_complexity'],
                'space_complexity': parsed['space_complexity'],
                'constraints': parsed['constraints']
            }
        }
    
    def save_to_json(self, task_spec: Dict[str, Any], output_path: str):
        """Save task specification to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(task_spec, f, indent=2, ensure_ascii=False)
        print(f"✅ Task saved to: {output_path}")


def parse_leetcode_cli():
    """CLI interface for parsing LeetCode problems."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python leetcode_parser.py <problem_file> [output_file]")
        print("Or paste LeetCode problem and press Ctrl+D (Ctrl+Z on Windows)")
        return
    
    # Read from file or stdin
    if sys.argv[1] == '-':
        problem_text = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            problem_text = f.read()
    
    # Parse problem
    parser = LeetCodeParser()
    parsed = parser.parse_leetcode_problem(problem_text)
    
    # Convert to all languages
    languages = ['python', 'cpp', 'java', 'javascript']
    
    for lang in languages:
        task_spec = parser.convert_to_codesmith_format(parsed, lang)
        
        # Determine output filename
        if len(sys.argv) > 2:
            base_name = sys.argv[2].replace('.json', '')
            output_file = f"{base_name}_{lang}.json"
        else:
            title_slug = parsed['title'].lower().replace(' ', '_')
            output_file = f"{title_slug}_{lang}.json"
        
        parser.save_to_json(task_spec, output_file)
    
    print(f"\n✅ Generated task files for {len(languages)} languages!")


if __name__ == '__main__':
    parse_leetcode_cli()
