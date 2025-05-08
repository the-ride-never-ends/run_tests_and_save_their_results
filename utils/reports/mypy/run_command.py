"""
Utility function to run mypy type checking.
"""
import subprocess
from typing import Any, Dict


def run_command(configs: Dict[str, Any]) -> str:
    """
    Run mypy type checking and return the output.
    
    Args:
        configs: Configuration dictionary with type checking settings
        
    Returns:
        str: The output from mypy
        
    Raises:
        RuntimeError: If there's an error running mypy
    """
    cmd = ["mypy", "."]
    
    try:
        # Run mypy
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Return combined output and error
        return result.stdout + result.stderr
    except Exception as e:
        raise RuntimeError(f"Error running mypy: {e}")