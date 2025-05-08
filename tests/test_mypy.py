from pathlib import Path
import subprocess
import sys
import unittest


class TestMypy(unittest.TestCase):
    def test_mypy_passes_on_valid_code(self):
        """Test that mypy passes on valid typed code."""
        # Create a temporary file with valid typed code
        valid_code = """

def add_numbers(a: int, b: int) -> int:
    return a + b

def get_name(person: Dict[str, str]) -> str:
    return person["name"]

def process_items(items: List[int]) -> List[int]:
    return [item * 2 for item in items]

def may_return_none(value: bool) -> Optional[str]:
    if value:
        return "Value is True"
    return None
"""
        
        temp_file = Path("temp_valid.py")
        temp_file.write_text(valid_code)
        
        # Run mypy on the file
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(temp_file)], 
            capture_output=True,
            text=True
        )
        
        # Clean up
        temp_file.unlink()
        
        # If mypy finds no errors, return code should be 0
        self.assertEqual(result.returncode, 0, f"mypy failed: {result.stdout}")
        self.assertEqual(result.stdout.strip(), "", f"Expected no output but got: {result.stdout}")

    def test_mypy_fails_on_invalid_code(self):
        """Test that mypy correctly identifies type errors."""
        # Create a temporary file with type errors
        invalid_code = """

def add_numbers(a: int, b: int) -> str:
    return a + b  # Error: Returns int, not str

def process_strings(items: List[str]) -> List[int]:
    return items  # Error: Returns List[str], not List[int]
"""
        
        temp_file = Path("temp_invalid.py")
        temp_file.write_text(invalid_code)
        
        # Run mypy on the file
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(temp_file)], 
            capture_output=True,
            text=True
        )
        
        # Clean up
        temp_file.unlink()
        
        # mypy should identify errors, return code should be 1
        self.assertEqual(result.returncode, 1, "mypy should fail on invalid types")
        self.assertIn("Incompatible return value", result.stdout, f"Expected type error not found in: {result.stdout}")


if __name__ == "__main__":
    unittest.main()