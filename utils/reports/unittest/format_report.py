"""
Utility function to format unittest results into a markdown report.
"""
from datetime import datetime
from typing import Any, List, Dict


def format_report(results: Any) -> List[str]:
    """
    Generate a Markdown report of the unittest results.
    
    Args:
        results: Results object containing test data
        
    Returns:
        List[str]: Lines of the markdown report
    """
    # Format timestamp
    timestamp = datetime.fromisoformat(results.timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    # Build markdown content
    content: List[str] = [
        "# Test Generator - Test Report",
        f"Generated on: {timestamp}\n",
        "## Summary",
        f"- **Tests Run**: {results.tests}",
        f"- **Passed**: {results.tests - results.failures - results.errors}",
        f"- **Failures**: {results.failures}",
        f"- **Errors**: {results.errors}",
        f"- **Skipped**: {results.skipped}",
        f"- **Expected Failures**: {results.expected_failures}",
        f"- **Unexpected Successes**: {results.unexpected_successes}",
        f"- **Success Rate**: {results.success_rate:.2f}%",
        f"- **Duration**: {results.duration} seconds",
        "",
    ]
    
    # Add test details if there are any issues
    if results.test_cases:
        content.extend([
            "## Test Details\n",
            "| Status | Module | Class | Test |",
            "|--------|--------|-------|------|",
        ])
        
        for test_case in results.test_cases:
            status = str(test_case.get("status", ""))
            module = str(test_case.get("module", ""))
            cls = str(test_case.get("class", ""))
            name = str(test_case.get("name", ""))
            
            content.append(f"| {status} | {module} | {cls} | {name} |")
        
        # Add failure/error details
        failures_or_errors = [tc for tc in results.test_cases if tc.get("status") in ("FAIL", "ERROR")]
        if failures_or_errors:
            content.append("\n## Failure and Error Details\n")
            
            for tc in failures_or_errors:
                tc_status = str(tc.get("status", ""))
                tc_module = str(tc.get("module", ""))
                tc_class = str(tc.get("class", ""))
                tc_name = str(tc.get("name", ""))
                tc_message = str(tc.get("message", ""))
                tc_traceback = str(tc.get("traceback", ""))
                
                content.extend([
                    f"### {tc_status}: {tc_module}.{tc_class}.{tc_name}",
                    f"**Message**: {tc_message}",
                    f"```\n{tc_traceback.strip()}\n```\n",
                ])
    
    return content