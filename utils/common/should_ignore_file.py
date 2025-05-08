import os
import re
from typing import Optional


#import pathspec
#Optional[pathspec.PathSpec]


def should_ignore_file(file_path: str, spec=None) -> bool:
    """
    Check if a file should be ignored based on gitignore patterns or if it's in a venv directory.

    Args:
        file_path: The file path to check
        spec: The PathSpec object with gitignore patterns

    Returns:
        True if the file should be ignored, False otherwise
    """
    # Always ignore files in any directory named 'venv'
    if re.search(r'(?:^|/|\\)venv(?:/|\\|$)', file_path):
        return True
    else:
        return False

    # if spec is None:
    #     return False

    # # Convert to path relative to the project root
    # rel_path = os.path.relpath(file_path, '.')

    # # Check if the file matches any gitignore pattern
    # return spec.match_file(rel_path)
