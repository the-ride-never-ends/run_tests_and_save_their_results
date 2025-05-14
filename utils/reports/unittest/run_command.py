"""
Utility function to run unittest tests through subprocess.
"""
import os
import subprocess
from pathlib import Path
from typing import Any


from logger import logger
from configs import Configs


def run_command(configs: Configs) -> Any:
    """
    Run the unittest tests using a subprocess call to bash script.
    
    Args:
        configs: Configuration dataclass with test_dir and other settings
        
    Returns:
        unittest.TestResult: The result of running the tests
        
    Raises:
        ValueError: If the operating system is not supported
        RuntimeError: If the subprocess command fails
    """

    # Ensure test_dir_path is a Path object
    test_dir = Path(configs.test_dir).resolve()
    project_root = test_dir.parent.resolve()

    # Check for the location of the unittest shell script
    script_path = Path(f"{configs.ROOT_DIR}/reports/services/_unittest.sh")
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
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0: # This should cause the try-except to be called.
            raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
        logger.debug(f"Command output: {result.stdout}")

        # Return the combined output and error
        # This should happen if all tests pass.
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e: # NOTE This should be called if any of the tests fail.
        if e.returncode != 0:
            if "FAILED" in e.stdout:
                return e.stdout + e.stderr
            else:
                raise RuntimeError(f"Command failed with exit code {e.returncode}\nstdout: {e.stdout}\nstderr: {e.stderr}\n") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"Command timed out: {e}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e