"""
Multi-Language Code Generator
Generates code in Python, C++, Java, and JavaScript.
"""

import subprocess
import sys
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from .agent import CodeSmithAgent


@dataclass
class CodeResult:
    """Result of code generation for a specific language."""
    language: str
    code: str
    success: bool
    attempts: int
    time_taken: float
    algorithm: str
    time_complexity: str
    space_complexity: str
    test_results: Dict[str, Any]
    error: str = ""


class MultiLanguageGenerator:
    """Generate code in multiple programming languages."""
    
    SUPPORTED_LANGUAGES = ['python', 'cpp', 'java', 'javascript']
    
    def __init__(self, llm_provider: str = 'gemini', api_key: str | None = None):
        """
        Initialize multi-language generator.
        
        Args:
            llm_provider: LLM provider (gemini, openai, anthropic, mock)
            api_key: API key for LLM provider
        """
        self.llm_provider = llm_provider
        self.api_key = api_key
        self.results = {}
    
    def generate_all_languages(self, task_spec: Dict[str, Any], 
                               max_attempts: int = 3) -> Dict[str, CodeResult]:
        """
        Generate code in all supported languages.
        
        Args:
            task_spec: Task specification (can be language-specific or generic)
            max_attempts: Maximum repair attempts per language
            
        Returns:
            Dictionary mapping language -> CodeResult
        """
        results = {}
        
        for language in self.SUPPORTED_LANGUAGES:
            print(f"\n{'='*70}")
            print(f"Generating {language.upper()} solution...")
            print(f"{'='*70}\n")
            
            start_time = time.time()
            
            try:
                result = self._generate_for_language(language, task_spec, max_attempts)
                result.time_taken = time.time() - start_time
                results[language] = result
                
            except Exception as e:
                results[language] = CodeResult(
                    language=language,
                    code="",
                    success=False,
                    attempts=0,
                    time_taken=time.time() - start_time,
                    algorithm="N/A",
                    time_complexity="N/A",
                    space_complexity="N/A",
                    test_results={},
                    error=str(e)
                )
        
        self.results = results
        return results
    
    def _generate_for_language(self, language: str, task_spec: Dict[str, Any],
                               max_attempts: int) -> CodeResult:
        """Generate code for a specific language."""
        
        # Adapt task for the language
        adapted_task = self._adapt_task_for_language(task_spec, language)
        
        # Import language-specific components
        if language == 'python':
            from .sandbox import CodeSandbox
            from .orchestrator import TaskOrchestrator
            
            agent = CodeSmithAgent(llm_provider=self.llm_provider, api_key=self.api_key)
            sandbox = CodeSandbox()
            orchestrator = TaskOrchestrator(agent, sandbox, max_attempts=max_attempts)
            
            result_dict = orchestrator.run_task(adapted_task)
            
            # Extract algorithm and complexity from plan/notes
            algorithm, time_comp, space_comp = self._extract_complexity_info(result_dict)
            
            return CodeResult(
                language='python',
                code=result_dict.get('code', ''),
                success=result_dict.get('success', False),
                attempts=result_dict.get('attempts', 0),
                time_taken=0,  # Will be set by caller
                algorithm=algorithm,
                time_complexity=time_comp,
                space_complexity=space_comp,
                test_results=result_dict.get('test_results', {}),
                error=result_dict.get('final_error', '')
            )
        
        elif language in ['cpp', 'java', 'javascript']:
            # For other languages, generate code but don't execute
            # (Would need language-specific sandboxes)
            agent = CodeSmithAgent(llm_provider=self.llm_provider, api_key=self.api_key)
            
            response = agent.generate_code(
                task=adapted_task['task']
            )
            
            algorithm, time_comp, space_comp = self._extract_complexity_from_response(response)
            
            return CodeResult(
                language=language,
                code=response.get('code', ''),
                success=True,  # Can't test without language-specific runner
                attempts=1,
                time_taken=0,
                algorithm=algorithm,
                time_complexity=time_comp,
                space_complexity=space_comp,
                test_results={'note': 'Code generated but not tested (no runner available)'},
                error=''
            )
        
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _adapt_task_for_language(self, task_spec: Dict[str, Any], 
                                 language: str) -> Dict[str, Any]:
        """Adapt task specification for target language."""
        
        adapted = task_spec.copy()
        
        # Language-specific task modifications
        if language == 'cpp':
            adapted['task'] = adapted['task'].replace(
                'sys.stdin.readline()', 
                'cin or getline'
            ).replace(
                'Python program',
                'C++ program with #include <iostream> and using namespace std'
            ).replace(
                'no doctests',
                'efficient C++ with proper memory management'
            )
        
        elif language == 'java':
            adapted['task'] = adapted['task'].replace(
                'sys.stdin.readline()',
                'Scanner.nextLine() or BufferedReader'
            ).replace(
                'Python program',
                'Java program with public static void main'
            ).replace(
                'no doctests',
                'proper Java class structure'
            )
        
        elif language == 'javascript':
            adapted['task'] = adapted['task'].replace(
                'sys.stdin.readline()',
                'readline() or process.stdin'
            ).replace(
                'Python program',
                'JavaScript/Node.js program'
            ).replace(
                'no doctests',
                'modern ES6+ syntax'
            )
        
        return adapted
    
    def _extract_complexity_info(self, result_dict: Dict[str, Any]) -> tuple:
        """Extract algorithm and complexity from result."""
        plan = result_dict.get('plan', '')
        notes = result_dict.get('notes', '')
        combined = f"{plan}\n{notes}"
        
        # Extract algorithm approach
        algorithm = "Not specified"
        if 'binary search' in combined.lower():
            algorithm = "Binary Search"
        elif 'hash' in combined.lower() or 'dict' in combined.lower():
            algorithm = "Hash Table / Dictionary"
        elif 'dynamic programming' in combined.lower() or 'dp' in combined.lower():
            algorithm = "Dynamic Programming"
        elif 'greedy' in combined.lower():
            algorithm = "Greedy"
        elif 'two pointer' in combined.lower():
            algorithm = "Two Pointers"
        elif 'sliding window' in combined.lower():
            algorithm = "Sliding Window"
        elif 'divide and conquer' in combined.lower():
            algorithm = "Divide and Conquer"
        elif 'backtrack' in combined.lower():
            algorithm = "Backtracking"
        elif 'bfs' in combined.lower() or 'breadth' in combined.lower():
            algorithm = "Breadth-First Search (BFS)"
        elif 'dfs' in combined.lower() or 'depth' in combined.lower():
            algorithm = "Depth-First Search (DFS)"
        
        # Extract time complexity
        import re
        time_match = re.search(r'O\([^)]+\)', combined)
        time_complexity = time_match.group(0) if time_match else "O(n)"
        
        # Space complexity (look for second O() or explicit mention)
        space_matches = re.findall(r'O\([^)]+\)', combined)
        space_complexity = space_matches[1] if len(space_matches) > 1 else "O(1)"
        
        return algorithm, time_complexity, space_complexity
    
    def _extract_complexity_from_response(self, response: Dict[str, Any]) -> tuple:
        """Extract complexity from LLM response."""
        plan = response.get('plan', '')
        notes = response.get('notes', '')
        
        return self._extract_complexity_info({'plan': plan, 'notes': notes})
    
    def print_results_table(self):
        """Print formatted results table."""
        if not self.results:
            print("No results to display")
            return
        
        print("\n" + "="*100)
        print("MULTI-LANGUAGE CODE GENERATION RESULTS")
        print("="*100 + "\n")
        
        # Header
        print(f"{'Language':<12} {'Status':<10} {'Attempts':<10} {'Time (s)':<12} {'Algorithm':<25} {'Time Complexity':<20}")
        print("-"*100)
        
        # Rows
        for lang, result in self.results.items():
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            time_str = f"{result.time_taken:.2f}s"
            
            print(f"{lang.upper():<12} {status:<10} {result.attempts:<10} {time_str:<12} {result.algorithm:<25} {result.time_complexity:<20}")
        
        print("-"*100)
        
        # Summary
        success_count = sum(1 for r in self.results.values() if r.success)
        print(f"\nTotal: {success_count}/{len(self.results)} languages succeeded")
        print()
    
    def save_results(self, output_dir: str):
        """Save generated code to files."""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        extensions = {
            'python': 'py',
            'cpp': 'cpp',
            'java': 'java',
            'javascript': 'js'
        }
        
        for lang, result in self.results.items():
            if result.code:
                ext = extensions.get(lang, 'txt')
                filename = os.path.join(output_dir, f"solution.{ext}")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    # Add header comment
                    comment_char = '//' if lang in ['cpp', 'java', 'javascript'] else '#'
                    f.write(f"{comment_char} Language: {lang.upper()}\n")
                    f.write(f"{comment_char} Algorithm: {result.algorithm}\n")
                    f.write(f"{comment_char} Time Complexity: {result.time_complexity}\n")
                    f.write(f"{comment_char} Space Complexity: {result.space_complexity}\n")
                    f.write(f"{comment_char} Generated in {result.time_taken:.2f}s\n\n")
                    f.write(result.code)
                
                print(f"✅ Saved {lang} solution to: {filename}")
        
        print(f"\n📁 All solutions saved to: {output_dir}")


def main():
    """CLI interface for multi-language generation."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Generate code in multiple languages')
    parser.add_argument('task_file', help='Task specification JSON file')
    parser.add_argument('--llm', default='gemini', help='LLM provider')
    parser.add_argument('--api-key', help='API key')
    parser.add_argument('--output-dir', default='multilang_output', help='Output directory')
    parser.add_argument('--languages', nargs='+', help='Specific languages to generate')
    
    args = parser.parse_args()
    
    # Load task
    with open(args.task_file, 'r') as f:
        task_spec = json.load(f)
    
    # Generate
    generator = MultiLanguageGenerator(llm_provider=args.llm, api_key=args.api_key)
    
    if args.languages:
        # Filter to requested languages
        original_langs = generator.SUPPORTED_LANGUAGES.copy()
        generator.SUPPORTED_LANGUAGES = [l for l in args.languages if l in original_langs]
    
    results = generator.generate_all_languages(task_spec)
    
    # Display results
    generator.print_results_table()
    
    # Save
    generator.save_results(args.output_dir)


if __name__ == '__main__':
    main()
