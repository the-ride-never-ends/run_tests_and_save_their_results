"""
Utility function to parse the output of unittest test runs.
"""
import re
import time
from typing import Any, Dict, Optional


def parse_output(output: str, results: Any) -> bool:
    """
    Parse the output from the unittest run and populate the results object.
    
    Args:
        output: String output from the unittest run
        results: Results object to populate
        
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Initialize results
    results.tests = 0
    results.errors = 0
    results.failures = 0
    results.skipped = 0
    results.expected_failures = 0
    results.unexpected_successes = 0
    results.test_cases = []
    
    # Extract test count using regex
    test_count_match = re.search(r'Ran (\d+) tests', output)
    if test_count_match:
        results.tests = int(test_count_match.group(1))
    
    # Check if tests were successful
    success = "OK" in output
    
    # Extract failures and errors
    error_match = re.search(r'FAILED \((.+?)\)', output)
    if error_match:
        error_info = error_match.group(1)
        
        # Extract error count
        errors_match = re.search(r'errors=(\d+)', error_info)
        if errors_match:
            results.errors = int(errors_match.group(1))
        
        # Extract failure count
        failures_match = re.search(r'failures=(\d+)', error_info)
        if failures_match:
            results.failures = int(failures_match.group(1))
            
        # Extract skipped count
        skipped_match = re.search(r'skipped=(\d+)', error_info)
        if skipped_match:
            results.skipped = int(skipped_match.group(1))
            
        # Extract expected failures count
        expected_failures_match = re.search(r'expected failures=(\d+)', error_info)
        if expected_failures_match:
            results.expected_failures = int(expected_failures_match.group(1))
            
        # Extract unexpected successes count
        unexpected_successes_match = re.search(r'unexpected successes=(\d+)', error_info)
        if unexpected_successes_match:
            results.unexpected_successes = int(unexpected_successes_match.group(1))
    
    # Calculate success rate
    if results.tests > 0:
        success_count = results.tests - results.errors - results.failures
        results.success_rate = (success_count / results.tests) * 100
    else:
        results.success_rate = 0
    
    # Parse individual test failures/errors from traceback sections
    test_failures = _extract_test_failures(output)
    for failure in test_failures:
        results.test_cases.append(failure)
    
    return success


def _extract_test_failures(output: str) -> list:
    """
    Extract individual test failures from unittest output.
    
    Args:
        output: String output from unittest
        
    Returns:
        list: List of test failure dictionaries
    """
    failure_sections = re.findall(r'======================================================================\n(FAIL|ERROR): (.+?)\n----------------------------------------------------------------------\n(.+?)(?=\n======================================================================|\Z)', 
                                output, re.DOTALL)
    
    test_failures = []
    for status, test_id, traceback in failure_sections:
        # Parse test_id into module, class, and method
        parts = test_id.split('.')
        if len(parts) >= 3:
            module = '.'.join(parts[:-2])
            class_name = parts[-2]
            method_name = parts[-1]
        else:
            module = parts[0] if parts else ""
            class_name = parts[1] if len(parts) > 1 else ""
            method_name = parts[2] if len(parts) > 2 else test_id
        
        # Extract error message from traceback
        message_match = re.search(r'\n([^\n]+)$', traceback.strip())
        message = message_match.group(1) if message_match else "Unknown error"
        
        test_failures.append({
            "id": test_id,
            "name": method_name,
            "module": module,
            "class": class_name,
            "status": status,
            "message": message,
            "traceback": traceback
        })
    
    return test_failures