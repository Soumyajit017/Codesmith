"""
CodeSmith Agent - Generates structured JSON responses for code tasks.
"""

import json
from typing import Dict, Any, Optional


class CodeSmithAgent:
    """
    Simulates a CodeSmith agent that produces JSON with plan/code/notes.
    In production, this would call an LLM API.
    """
    
    def __init__(self, llm_provider: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize CodeSmith agent.
        
        Args:
            llm_provider: 'mock', 'openai', 'anthropic', 'gemini', or None for mock
            api_key: API key for the provider (optional, can use env var)
        """
        self.llm_provider = llm_provider or 'mock'
        self.api_key = api_key
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load the CodeSmith system prompt."""
        return """You are CodeSmith, a Python Coding Agent designed to autonomously write, test, and repair Python code for small engineering tasks.

Your job is to reason explicitly (internally) but output only a structured JSON that the host program can parse.
Always obey the schema and never add prose or commentary outside JSON.

JSON Output Format:
{
  "plan": "Explain approach, algorithms, data structures, edge cases.",
  "code": "Full Python 3 script including imports, functions, and main().",
  "notes": "Any quick remarks, such as test usage, CLI hints, or caveats."
}

Coding Guidelines:
- Python version: 3.10+
- Include minimal, readable functions
- Include doctests (3–5 examples inside docstrings)
- Include CLI entrypoint (so user can run: python main.py)
- Use clean imports (standard library preferred)
- Avoid heavy external libraries, OS access, file writes unless explicitly told
- Follow PEP-8 indentation (4 spaces)
- Return exact JSON (parsable by json.loads)

Never include markdown formatting, triple backticks, or natural language outside JSON.
"""
    
    def generate_code(self, task: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate code for a task, optionally with repair feedback.
        
        Args:
            task: Task description
            feedback: Optional feedback from previous execution/tests
            
        Returns:
            Dict with keys: plan, code, notes
        """
        if self.llm_provider == 'mock':
            return self._mock_generate(task, feedback)
        elif self.llm_provider == 'openai':
            return self._openai_generate(task, feedback)
        elif self.llm_provider == 'anthropic':
            return self._anthropic_generate(task, feedback)
        elif self.llm_provider == 'gemini':
            return self._gemini_generate(task, feedback)
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
    
    def _mock_generate(self, task: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """Mock implementation for testing without LLM."""
        from .templates import get_template
        
        # Detect language and problem type
        task_lower = task.lower()
        
        # Detect language (order matters - check javascript before java!)
        language = 'python'
        if 'c++' in task_lower:
            language = 'cpp'
        elif 'javascript' in task_lower or ' js ' in task_lower:
            language = 'javascript'
        elif 'java' in task_lower:
            language = 'java'
        
        # Detect problem type
        if 'two sum' in task_lower or ('sum' in task_lower and 'target' in task_lower):
            template = get_template(language, 'two_sum')
            if template:
                return {
                    "plan": "Use hash table to find two numbers that sum to target in O(n) time",
                    "code": template,
                    "notes": "Hash Table algorithm with O(n) time and O(n) space complexity"
                }
        
        # Fall back to original Python-only patterns
        if language != 'python':
            # For non-Python without template, return generic code
            return {
                "plan": f"Generate {language} solution",
                "code": f"// {language.upper()} code would be generated here by real LLM\n// This is just a mock placeholder",
                "notes": f"{language} code generation requires real LLM"
            }
        
        # Original Python patterns
        task_lower = task.lower()
        
        if 'fibonacci' in task_lower:
            return {
                "plan": "Generate Fibonacci up to N using iterative method; handle N=0 or 1; print joined list.",
                "code": '''def fib(n):
    """Return first n Fibonacci numbers.
    
    >>> fib(5)
    [0, 1, 1, 2, 3]
    >>> fib(0)
    []
    >>> fib(1)
    [0]
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    a, b = 0, 1
    res = [a]
    for _ in range(n - 1):
        res.append(b)
        a, b = b, a + b
    return res

if __name__ == '__main__':
    import sys
    n = int(sys.stdin.readline().strip())
    print(' '.join(map(str, fib(n))))
''',
                "notes": "Simple iterative Fibonacci. Works for small N. Can add memoization for larger inputs."
            }
        
        elif 'mean' in task_lower or 'average' in task_lower:
            return {
                "plan": "Parse CSV line, convert to integers, compute mean, round to 2 decimals. Handle empty input.",
                "code": '''def compute_mean(csv_line):
    """Compute mean of comma-separated integers.
    
    >>> compute_mean("1,2,3,4,5")
    3.0
    >>> compute_mean("10,20,30")
    20.0
    >>> compute_mean("7")
    7.0
    """
    nums = [int(x.strip()) for x in csv_line.split(',') if x.strip()]
    if not nums:
        return 0.0
    return round(sum(nums) / len(nums), 2)

if __name__ == '__main__':
    import sys
    line = sys.stdin.readline().strip()
    print(compute_mean(line))
''',
                "notes": "Handles whitespace and empty values. Returns 0.0 for empty input."
            }
        
        elif 'palindrome' in task_lower:
            return {
                "plan": "Check if string reads same forwards and backwards. Ignore case and spaces.",
                "code": '''def is_palindrome(s):
    """Check if string is palindrome.
    
    >>> is_palindrome("racecar")
    True
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("A man a plan a canal Panama")
    True
    >>> is_palindrome("")
    True
    """
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

if __name__ == '__main__':
    import sys
    text = sys.stdin.readline().strip()
    result = is_palindrome(text)
    print("true" if result else "false")
''',
                "notes": "Ignores spaces, punctuation, and case. Empty string is palindrome."
            }
        
        elif 'sum' in task_lower or 'add' in task_lower:
            # Check if it's asking for two numbers
            if 'two' in task_lower or 'separate' in task_lower:
                return {
                    "plan": "Read two integers from separate lines, compute sum, print result.",
                    "code": '''def add_two_numbers():
    """Add two numbers from input.
    
    >>> # Interactive test not suitable for doctest
    """
    import sys
    a = int(sys.stdin.readline().strip())
    b = int(sys.stdin.readline().strip())
    return a + b

if __name__ == '__main__':
    result = add_two_numbers()
    print(result)
''',
                    "notes": "Reads two integers from stdin and prints their sum."
                }
            else:
                return {
                    "plan": "Parse numbers and compute sum.",
                    "code": '''def compute_sum(line):
    """Compute sum of space-separated integers."""
    nums = [int(x) for x in line.split()]
    return sum(nums)

if __name__ == '__main__':
    import sys
    line = sys.stdin.readline().strip()
    print(compute_sum(line))
''',
                    "notes": "Simple sum of space-separated numbers."
                }
        
        else:
            # Generic template
            return {
                "plan": "Parse task requirements; implement solution with proper error handling; add doctests.",
                "code": '''def solve():
    """Generic solution template.
    
    >>> solve()
    'Solution'
    """
    return "Solution"

if __name__ == '__main__':
    import sys
    result = solve()
    print(result)
''',
                "notes": "Generic template - needs customization for specific task."
            }
    
    def _openai_generate(self, task: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """Generate using OpenAI API."""
        try:
            import openai
            
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if feedback:
                messages.append({
                    "role": "user",
                    "content": f"Previous attempt failed with feedback:\n{feedback}\n\nPlease fix the code."
                })
            else:
                messages.append({
                    "role": "user",
                    "content": f"Task:\n{task}"
                })
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")
    
    def _anthropic_generate(self, task: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """Generate using Anthropic Claude API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic()
            
            user_message = f"Task:\n{task}"
            if feedback:
                user_message = f"Previous attempt failed with feedback:\n{feedback}\n\nPlease fix the code."
            
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2048,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            content = message.content[0].text
            return json.loads(content)
            
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {e}")
    
    def _gemini_generate(self, task: str, feedback: Optional[str] = None) -> Dict[str, Any]:
        """Generate using Google Gemini API."""
        try:
            import google.generativeai as genai
            
            # Configure API key
            if self.api_key:
                genai.configure(api_key=self.api_key)
            else:
                import os
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY env var or pass api_key parameter.")
                genai.configure(api_key=api_key)
            
            # Create model
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Build prompt
            prompt = f"{self.system_prompt}\n\n"
            if feedback:
                prompt += f"Previous attempt failed with feedback:\n{feedback}\n\nPlease fix the code.\n\n"
            prompt += f"Task:\n{task}\n\nRespond with valid JSON only (no markdown, no code blocks):"
            
            # Generate
            response = model.generate_content(prompt)
            
            # Extract JSON from response
            content = response.text.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                # Remove first and last lines if they are code fence markers
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                content = '\n'.join(lines)
            
            # Try to parse JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError(f"Could not parse JSON from response: {content[:200]}")
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")
