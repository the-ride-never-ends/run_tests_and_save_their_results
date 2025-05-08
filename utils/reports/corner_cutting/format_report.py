"""
Utility function to format corner-cutting results into a markdown report.
"""
from datetime import datetime
from typing import Any, List, Dict
from collections import defaultdict


def format_report(results: Any) -> List[str]:
    """
    Generate a Markdown report of the corner-cutting scan results.
    
    Args:
        results: Results object containing corner-cutting data
        
    Returns:
        List[str]: Lines of the markdown report
    """
    # Format timestamp
    timestamp = datetime.fromisoformat(results.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    # Build markdown content
    content: List[str] = [
        "# Code Corner-Cutting Analysis Report\n",
        f"Generated on: {timestamp}\n",
        "## Summary\n",
        f"- **Files Scanned**: {results.total_files_scanned}",
        f"- **Potential Corner-Cutting Instances**: {results.total_potential_instances}",
        "",
    ]
    
    # If issues were found, add detailed sections
    if results.corner_cutting:
        content.append("## Issues by Category\n")
        
        # Group issues by category
        categories = defaultdict(list)
        for issue in results.corner_cutting:
            categories[issue.get("category", "Unknown")].append(issue)
            
        # Add each category
        for category, issues in categories.items():
            content.append(f"### {category} ({len(issues)} instances)\n")
            
            # Group by file
            files = defaultdict(list)
            for issue in issues:
                files[issue.get("file", "Unknown")].append(issue)
            
            # Add each file
            for file, file_issues in files.items():
                content.append(f"#### {file}\n")
                
                for issue in file_issues:
                    line = issue.get("line", "")
                    message = issue.get("message", "")
                    snippet = issue.get("snippet", "")
                    
                    content.append(f"- Line {line}: {message}")
                    if snippet:
                        content.append(f"  ```python\n  {snippet}\n  ```")
                
                content.append("")
            
            content.append("")
    
    return content