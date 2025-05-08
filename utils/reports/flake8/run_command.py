"""
Utility function to run flake8 linting.
"""
import subprocess
from typing import Any, Dict


def run_command(configs: Dict[str, Any]) -> str:
    """
    Run flake8 linting and return the output.
    
    Args:
        configs: Configuration dictionary with linting settings
        
    Returns:
        str: The output from flake8
        
    Raises:
        RuntimeError: If there's an error running flake8
    """
    cmd = ["flake8"]
    
    try:
        # Run flake8
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Return combined output and error
        return result.stdout + result.stderr
    except Exception as e:
        raise RuntimeError(f"Error running flake8: {e}")