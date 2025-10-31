"""
Sandbox executor for running and testing generated code.
"""

import sys
import io
import traceback
import doctest
from typing import Dict, Any, Optional, Tuple


class CodeSandbox:
    """Executes code in a controlled environment and captures results."""
    
    def __init__(self, timeout: int = 5):
        """
        Initialize sandbox.
        
        Args:
            timeout: Execution timeout in seconds (not enforced in basic version)
        """
        self.timeout = timeout
    
    def execute(self, code: str, stdin_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute code and capture output.
        
        Args:
            code: Python code to execute
            stdin_input: Optional input to provide via stdin
            
        Returns:
            Dict with keys: success, stdout, stderr, error
        """
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_stdin = sys.stdin
        
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        if stdin_input is not None:
            sys.stdin = io.StringIO(stdin_input)
        
        result = {
            'success': False,
            'stdout': '',
            'stderr': '',
            'error': None
        }
        
        try:
            # Create isolated namespace
            namespace = {
                '__name__': '__main__',
                '__builtins__': __builtins__
            }
            
            # Execute code
            exec(code, namespace)
            
            result['success'] = True
            result['stdout'] = sys.stdout.getvalue()
            result['stderr'] = sys.stderr.getvalue()
            
        except Exception as e:
            result['success'] = False
            result['error'] = traceback.format_exc()
            result['stderr'] = sys.stderr.getvalue()
            
        finally:
            # Restore original streams
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.stdin = old_stdin
        
        return result
    
    def run_doctests(self, code: str) -> Dict[str, Any]:
        """
        Run doctests in the code.
        
        Args:
            code: Python code containing doctests
            
        Returns:
            Dict with keys: success, passed, failed, details
        """
        result = {
            'success': False,
            'passed': 0,
            'failed': 0,
            'details': ''
        }
        
        old_stdout = sys.stdout  # Save before try block
        
        try:
            # Create module from code
            namespace = {}
            exec(code, namespace)
            
            # Run doctests with output capture
            import doctest
            sys.stdout = io.StringIO()
            
            finder = doctest.DocTestFinder()
            runner = doctest.DocTestRunner(verbose=False)
            
            tests_run = 0
            for name, obj in namespace.items():
                if callable(obj) and hasattr(obj, '__doc__') and obj.__doc__:
                    tests = finder.find(obj, name=name)
                    for test in tests:
                        if test.examples:  # Only run if there are actual tests
                            tests_run += 1
                            runner.run(test)
            
            # Get results
            passed, failed = runner.summarize(verbose=False)
            
            result['passed'] = passed
            result['failed'] = failed
            result['success'] = (failed == 0 and tests_run > 0)
            result['details'] = sys.stdout.getvalue()
            
            sys.stdout = old_stdout
            
        except Exception as e:
            result['success'] = False
            result['details'] = f"Doctest error: {traceback.format_exc()}"
            try:
                sys.stdout = old_stdout
            except:
                pass
        
        return result
    
    def validate_output(self, code: str, test_cases: list) -> Dict[str, Any]:
        """
        Validate code against test cases.
        
        Args:
            code: Python code to test
            test_cases: List of dicts with 'input' and 'expected' keys
            
        Returns:
            Dict with keys: success, passed, failed, failures
        """
        result = {
            'success': True,
            'passed': 0,
            'failed': 0,
            'failures': []
        }
        
        for i, test in enumerate(test_cases):
            stdin_input = test.get('input')
            expected = test.get('expected')
            
            exec_result = self.execute(code, stdin_input)
            
            if not exec_result['success']:
                result['success'] = False
                result['failed'] += 1
                result['failures'].append({
                    'test_id': i,
                    'input': stdin_input,
                    'expected': expected,
                    'error': exec_result['error']
                })
            else:
                actual = exec_result['stdout'].strip()
                if actual == expected.strip():
                    result['passed'] += 1
                else:
                    result['success'] = False
                    result['failed'] += 1
                    result['failures'].append({
                        'test_id': i,
                        'input': stdin_input,
                        'expected': expected,
                        'actual': actual
                    })
        
        return result
