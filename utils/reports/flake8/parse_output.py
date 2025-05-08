"""
Utility function to parse flake8 output and update results.
"""
from typing import Any


def parse_output(output: str, results: Any) -> bool:
    """
    Parse flake8 output and update results.
    
    Args:
        output: String output from flake8
        results: Results object to update
        
    Returns:
        bool: True if no issues found, False otherwise
    """
    # Reset error count
    error_count = 0
    results.issues = []
    
    # Parse each line of output
    for line in output.strip().split('\n'):
        if not line:
            continue
        
        error_count += 1
        
        # Try to parse the error line
        try:
            # Format is typically: ./file.py:line:col: code message
            parts = line.split(':', 3)
            
            if len(parts) >= 4:
                file_path = parts[0]
                line_num = parts[1]
                col_num = parts[2]
                code_message = parts[3].strip().split(' ', 1)
                
                results.issues.append({
                    "file": file_path,
                    "line": line_num,
                    "column": col_num,
                    "error_code": code_message[0] if len(code_message) > 0 else "",
                    "message": code_message[1] if len(code_message) > 1 else ""
                })
            else:
                # If we can't parse it, just add the whole line
                results.issues.append({
                    "message": line
                })
        except Exception:
            # If any parsing error, just add the whole line
            results.issues.append({
                "message": line
            })
    
    # Update result fields
    results.errors = error_count
    results.status = "pass" if error_count == 0 else "fail"
    
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
    
    return results.errors == 0