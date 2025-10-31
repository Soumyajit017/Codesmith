"""
Task orchestrator - manages the task loop with feedback and repairs.
"""

import json
from typing import Dict, Any, List, Optional
from .agent import CodeSmithAgent
from .sandbox import CodeSandbox


class TaskOrchestrator:
    """Orchestrates the task execution loop with repairs."""
    
    def __init__(self, agent: CodeSmithAgent, sandbox: CodeSandbox, max_attempts: int = 3):
        """
        Initialize orchestrator.
        
        Args:
            agent: CodeSmith agent for code generation
            sandbox: Sandbox for code execution
            max_attempts: Maximum repair attempts
        """
        self.agent = agent
        self.sandbox = sandbox
        self.max_attempts = max_attempts
    
    def run_task(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a complete task with repair loop.
        
        Args:
            task_spec: Dict with keys:
                - task: Task description
                - test_cases: List of test cases (optional)
                - run_doctests: Whether to run doctests (default True)
                
        Returns:
            Dict with execution history and final result
        """
        task = task_spec['task']
        test_cases = task_spec.get('test_cases', [])
        run_doctests = task_spec.get('run_doctests', True)
        
        history = []
        feedback = None
        
        for attempt in range(self.max_attempts):
            print(f"\n{'='*60}")
            print(f"Attempt {attempt + 1}/{self.max_attempts}")
            print(f"{'='*60}")
            
            # Generate code
            try:
                response = self.agent.generate_code(task, feedback)
                
                # Validate JSON structure
                if not all(k in response for k in ['plan', 'code', 'notes']):
                    raise ValueError("Invalid response structure - missing required keys")
                
                plan = response['plan']
                code = response['code']
                notes = response['notes']
                
                print(f"\nPlan: {plan}")
                print(f"\nNotes: {notes}")
                print(f"\nCode generated ({len(code)} chars)")
                
            except Exception as e:
                history.append({
                    'attempt': attempt + 1,
                    'error': f"Agent error: {str(e)}",
                    'success': False
                })
                feedback = f"Failed to generate valid code: {str(e)}"
                continue
            
            # Run doctests if requested
            doctest_result = None
            if run_doctests:
                print("\nRunning doctests...")
                doctest_result = self.sandbox.run_doctests(code)
                print(f"Doctests: {doctest_result['passed']} passed, {doctest_result['failed']} failed")
                
                if not doctest_result['success']:
                    print("Doctest failures detected")
            
            # Run test cases if provided
            test_result = None
            if test_cases:
                print(f"\nRunning {len(test_cases)} test cases...")
                test_result = self.sandbox.validate_output(code, test_cases)
                print(f"Tests: {test_result['passed']} passed, {test_result['failed']} failed")
                
                if not test_result['success']:
                    print("Test failures detected")
            
            # Record attempt
            attempt_record = {
                'attempt': attempt + 1,
                'plan': plan,
                'code': code,
                'notes': notes,
                'doctest_result': doctest_result,
                'test_result': test_result,
                'success': True
            }
            
            # Check if all tests passed
            if run_doctests and doctest_result and not doctest_result['success']:
                attempt_record['success'] = False
                feedback = self._build_feedback(doctest_result, test_result, "doctests")
            elif test_cases and test_result and not test_result['success']:
                attempt_record['success'] = False
                feedback = self._build_feedback(doctest_result, test_result, "tests")
            else:
                # Success!
                history.append(attempt_record)
                print(f"\n✅ Task completed successfully on attempt {attempt + 1}")
                return {
                    'success': True,
                    'attempts': attempt + 1,
                    'history': history,
                    'final_code': code
                }
            
            history.append(attempt_record)
        
        # Max attempts reached
        print(f"\n❌ Task failed after {self.max_attempts} attempts")
        final_code = history[-1]['code'] if history and 'code' in history[-1] else None
        return {
            'success': False,
            'attempts': self.max_attempts,
            'history': history,
            'final_code': final_code
        }
    
    def _build_feedback(self, doctest_result: Optional[Dict], 
                       test_result: Optional[Dict],
                       failure_type: str) -> str:
        """Build feedback message for repair."""
        feedback_parts = []
        
        if failure_type == "doctests" and doctest_result:
            feedback_parts.append(f"Doctests failed: {doctest_result['failed']} failures")
            if doctest_result.get('details'):
                feedback_parts.append(f"Details:\n{doctest_result['details']}")
        
        if failure_type == "tests" and test_result:
            feedback_parts.append(f"Test cases failed: {test_result['failed']} failures")
            for failure in test_result.get('failures', []):
                if 'error' in failure:
                    feedback_parts.append(f"\nTest {failure['test_id']} error:\n{failure['error']}")
                else:
                    feedback_parts.append(
                        f"\nTest {failure['test_id']}:\n"
                        f"  Input: {failure['input']}\n"
                        f"  Expected: {failure['expected']}\n"
                        f"  Actual: {failure['actual']}"
                    )
        
        return "\n".join(feedback_parts)
