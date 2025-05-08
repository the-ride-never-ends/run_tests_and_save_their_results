"""
Utility function to parse mypy output and update results.
"""
import re
from typing import Any


def parse_output(output: str, results: Any) -> bool:
    """
    Parse mypy output and update results.
    
    Args:
        output: String output from mypy
        results: Results object to update
        
    Returns:
        bool: True if no issues found, False otherwise
    """
    # Reset issues
    results.issues = []
    error_count = 0
    
    # Define pattern to match mypy error lines
    # Format: file:line: error message  [error-code]
    error_pattern = r'([^:]+):(\d+)(?::(\d+))?: (?:error|warning|note): (.+?)(?:\s+\[([^\]]+)\])?$'
    
    # Parse each line of output
    for line in output.strip().split('\n'):
        if not line or line.startswith('Success:'):
            continue
        
        match = re.match(error_pattern, line)
        if match:
            file_path, line_num, col_num, message, error_code = match.groups()
            
            results.issues.append({
                "file": file_path,
                "line": line_num,
                "column": col_num or "",
                "error_code": error_code or "",
                "message": message
            })
            
            error_count += 1
        else:
            # Handle lines that don't match the pattern (e.g., summary lines)
            continue
    
    # Check for success message
    success = 'Success: no issues found' in output
    
    # Update result fields
    results.errors = error_count
    results.status = "pass" if success else "fail"
    
    # Apply gitignore filtering if requested
    if getattr(results, 'configs', None) and getattr(results.configs, 'respect_gitignore', False) and getattr(results.configs, 'gitignore_spec', None):
        from utils.common.should_ignore_file import should_ignore_file
        
        # Filter out issues in ignored files
        filtered_issues = []
        filtered_count = 0
        
        for issue in results.issues:
            file_path = issue.get("file", "")
            if file_path and should_ignore_file(file_path, results.configs.gitignore_spec):
                filtered_count += 1
            else:
                filtered_issues.append(issue)
        
        if filtered_count > 0:
            results.issues = filtered_issues
            results.errors -= filtered_count
    
    return success