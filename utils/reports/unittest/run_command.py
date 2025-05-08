"""
Utility function to run unittest tests through subprocess.
"""
import os
import subprocess
from pathlib import Path
from typing import Any, Dict


def run_command(configs: Dict[str, Any]) -> Any:
    """
    Run the unittest tests using a subprocess call to bash script.
    
    Args:
        configs: Configuration dictionary with test_dir and other settings
        
    Returns:
        unittest.TestResult: The result of running the tests
        
    Raises:
        ValueError: If the operating system is not supported
        RuntimeError: If the subprocess command fails
    """
    import sys
    
    # Ensure test_dir_path is a Path object
    test_dir = Path(configs.test_dir).resolve()
    project_root = test_dir.parent.resolve()
    this_dir = Path(__file__).parent.resolve()
    
    # Check for the location of the unittest shell script
    script_path = Path("/home/kylerose1946/claudes_toolbox/run_tests_and_save_their_results/reports/services/_unittest.sh")
    if not script_path.exists():
        raise FileNotFoundError(f"Unittest shell script not found at {script_path}")
    
    # Create the command based on OS
    if os.name == "posix":  # Linux/Mac
        cmd = ["bash", f"{script_path}", f"{project_root}"]
    elif os.name == "nt":  # Windows
        raise NotImplementedError("Windows support is not implemented yet.")
    else:
        raise ValueError(f"Unsupported operating system: {os.name}")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed with exit code {result.returncode}: {result.stderr}")
        
        # Return the combined output and error
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed with error: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")