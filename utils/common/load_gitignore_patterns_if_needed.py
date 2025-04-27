from pathlib import Path
from typing import Optional


import pathspec


def load_gitignore_patterns_if_needed(respect_gitignore: bool, reports_dir: Path) -> Optional[pathspec.PathSpec]:
    """
    Load patterns from a .gitignore file if respect_gitignore is True.

    This function reads patterns from a .gitignore file located in the parent directory
    of reports_dir and constructs a PathSpec object that can be used to match paths
    against these patterns.

    Args:
        respect_gitignore: Boolean indicating whether to respect .gitignore patterns.
        reports_dir: Path object pointing to the reports directory.

    Returns:
        A PathSpec object containing the patterns from .gitignore if respect_gitignore
        is True and the .gitignore file exists, None otherwise.
    """
    gitignore_spec = None

    if respect_gitignore:
        gitignore_path = reports_dir.parent / '.gitignore'

        if not gitignore_path.exists():
            return None

        with open(gitignore_path, 'r') as f:
            patterns = f.read().splitlines()

        gitignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)

        if gitignore_spec:
            print(f"Using gitignore patterns from {gitignore_path}.")

    return gitignore_spec