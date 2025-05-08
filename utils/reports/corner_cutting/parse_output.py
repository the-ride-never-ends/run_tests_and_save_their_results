"""
Utility function to parse corner-cutting scan results.
"""
from typing import Any, Dict


def parse_output(output: Dict[str, Any], results: Any) -> bool:
    """
    Process the corner-cutting scan results.
    
    Args:
        output: Dictionary with scan results
        results: Results object to update
        
    Returns:
        bool: True if no issues found, False otherwise
    """
    # Update results with scan statistics
    results.total_files_scanned = output.get("total_files_scanned", 0)
    results.total_potential_instances = len(output.get("issues", []))
    
    # Add all issues found to results
    results.corner_cutting = output.get("issues", [])
    
    # Set error count for summary
    results.errors = results.total_potential_instances
    
    # Set status
    results.status = "pass" if results.total_potential_instances == 0 else "fail"
    
    # Return success status
    return results.total_potential_instances == 0