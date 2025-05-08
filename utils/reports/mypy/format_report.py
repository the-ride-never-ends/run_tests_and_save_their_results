"""
Utility function to format mypy results into a markdown report.
"""
from datetime import datetime
from typing import Any, List, Dict


def format_report(results: Any) -> List[str]:
    """
    Generate a Markdown report of the mypy type checking results.
    
    Args:
        results: Results object containing type checking data
        
    Returns:
        List[str]: Lines of the markdown report
    """
    # Format timestamp
    timestamp = datetime.fromisoformat(results.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    # Build markdown content
    content: List[str] = [
        "# Type Checking Report - mypy\n",
        f"Generated on: {timestamp}\n",
        "## Summary\n",
        f"- **Type Checking (mypy)**: {results.status.upper()} ({results.errors} issues)\n",
    ]
    
    # Add mypy issues
    if results.issues:
        content.append("## Type Checking Issues (mypy)\n")
        
        # Group issues by file
        files_with_issues: Dict[str, List[Dict[str, Any]]] = {}
        for issue in results.issues:
            file_path = issue.get("file", "Unknown file")
            if file_path not in files_with_issues:
                files_with_issues[file_path] = []
            files_with_issues[file_path].append(issue)
        
        # Add issues by file
        for file_path, issues in files_with_issues.items():
            content.append(f"### {file_path}\n")
            
            for issue in issues:
                line = issue.get("line", "")
                column = issue.get("column", "")
                message = issue.get("message", "")
                error_code = issue.get("error_code", "")
                
                location = f"Line {line}"
                if column:
                    location += f", Col {column}"
                
                error_info = message
                if error_code:
                    error_info += f" [{error_code}]"
                
                content.append(f"- {location}: {error_info}")
            
            content.append("")
    
    return content