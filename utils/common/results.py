from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Results:
    """Class to hold the results of a test run."""
    # linting attributes
    name: str
    status: str = "not_run"
    errors: int = 0
    issues: list[dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # testing attributes
    tests: int = 0
    failures: int = 0
    skipped: int = 0
    expected_failures: int = 0
    unexpected_successes: int = 0
    success_rate: float = 0.0
    duration: float = 0.0
    test_cases: list[dict[str, Any]] = field(default_factory=list)

    # corner cutting attributes
    corner_cutting: list[dict[str, Any]] = field(default_factory=list)
    total_files_scanned: int = 0
    total_potential_instances: int = 0

    def to_dict(self) -> dict[str, Any]:
        match self.name:
            case "flake8" | "mypy":
                return {
                    "summary": {
                        f"{self.name}_errors": self.errors,
                        f"{self.name}_status": self.status,
                        "timestamp": self.timestamp,
                    },
                    f"{self.name}_issues": self.issues
                }
            case "unittest":
                return {
                    "summary": {
                        "tests": self.tests,
                        "errors": self.errors,
                        "failures": self.failures,
                        "skipped": self.skipped,
                        "expected_failures": self.expected_failures,
                        "unexpected_successes": self.unexpected_successes,
                        "success_rate": self.success_rate,
                        "duration": self.duration,
                        "timestamp": self.timestamp,
                    },
                    "test_cases": [] # {"id": "", "name": "", "module": "", "class": "", "status": "", "message": "", "traceback": ""}
                }
            case "corner_cutting":
                return {
                    "summary": {
                        "total_files_scanned": self.total_files_scanned,
                        "total_potential_instances": self.total_potential_instances,
                        "timestamp": self.timestamp,
                    },
                    "corner_cutting": [] # sub-dict {"file": "", "line": "", "message": "", }
                }
            case _:
                raise ValueError(f"Unknown collector name: {self.name}")