import os
from typing import Optional


import pathspec


def should_ignore_file(file_path: str, spec: Optional[pathspec.PathSpec]) -> bool:
    """
    Check if a file should be ignored based on gitignore patterns or if it's in a venv directory.

    Args:
        file_path: The file path to check
        spec: The PathSpec object with gitignore patterns

    Returns:
        True if the file should be ignored, False otherwise
    """
    # Always ignore files in any directory named 'venv'
    if '/venv/' in file_path or file_path.startswith('venv/') or file_path.endswith('/venv'):
        return True

    if spec is None:
        return False

    # Convert to path relative to the project root
    rel_path = os.path.relpath(file_path, '.')

    # Check if the file matches any gitignore pattern
    return spec.match_file(rel_path)
