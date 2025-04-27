from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


import pathspec


from utils.common.load_gitignore_patterns_if_needed import load_gitignore_patterns_if_needed


@dataclass
class Configs:
    """
    Configuration class for running tests and generating reports.
    
    Attributes:
        test_dir: Path to the directory containing tests to run
        reports_dir: Path to store generated reports
        respect_gitignore: Whether to ignore files matching gitignore patterns
        verbosity: Level of detail in test output
        gitignore_spec: PathSpec object containing gitignore patterns (set in post_init)
    """
    test_dir: Path
    reports_dir: Path
    respect_gitignore: bool
    verbosity: int
    gitignore_spec: Optional[pathspec.PathSpec] = None

    def __post_init__(self):
        # Ensure paths are absolute and exist.
        self.test_dir = self.test_dir.resolve()
        if not self.test_dir.exists:
            raise ValueError(f"Test directory '{self.test_dir}' does not exist.")

        self.reports_dir = self.reports_dir.resolve()
        if not self.reports_dir.exists():
            self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.gitignore_spec = load_gitignore_patterns_if_needed(self.respect_gitignore, self.reports_dir)

    def __getitem__(self, item: str) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(f"Key '{item}' not found in Configs")