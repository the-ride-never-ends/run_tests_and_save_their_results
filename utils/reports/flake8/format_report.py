"""
Utility function to format flake8 results into a markdown report.
"""
from datetime import datetime
from typing import Any, List, Dict


def format_report(results: Any) -> List[str]:
    """
    Generate a Markdown report of the flake8 linting results.
    
    Args:
        results: Results object containing linting data
        
    Returns:
        List[str]: Lines of the markdown report
    """
    # Format timestamp
    timestamp = datetime.fromisoformat(results.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    # Build markdown content
    content: List[str] = [
        "# Code Style Report - flake8\n",
        f"Generated on: {timestamp}\n",
        "## Summary\n",
        f"- **Code Style (flake8)**: {results.status.upper()} ({results.errors} issues)\n",
    ]
    
    # Add flake8 issues
    if results.issues:
        content.append("## Code Style Issues (flake8)\n")
        
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
                
                content.append(f"- {location}: {error_code} {message}")
            
            content.append("")
    
    return content