#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main CLI entry point for running tests and generating reports.
"""
import argparse
from datetime import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable


# Add local utils to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from configs import Configs
from logger import logger

from reports.collector import Collector
from reports.services.flake8 import Flake8Collector
from reports.services.mypy import MyPyCollector
from reports.services.corner_cutting import CornerCuttingCollector

# Import utility functions for collector resources
from utils.reports.unittest.run_command import run_command as unittest_run_command
from utils.reports.unittest.parse_output import parse_output as unittest_parse_output
from utils.reports.unittest.format_report import format_report as unittest_format_report

from utils.reports.flake8.run_command import run_command as flake8_run_command
from utils.reports.flake8.parse_output import parse_output as flake8_parse_output
from utils.reports.flake8.format_report import format_report as flake8_format_report

from utils.reports.mypy.run_command import run_command as mypy_run_command
from utils.reports.mypy.parse_output import parse_output as mypy_parse_output
from utils.reports.mypy.format_report import format_report as mypy_format_report

from utils.reports.corner_cutting.run_command import run_command as corner_cutting_run_command
from utils.reports.corner_cutting.parse_output import parse_output as corner_cutting_parse_output
from utils.reports.corner_cutting.format_report import format_report as corner_cutting_format_report


class RunTestsAndSaveTheirResults:

    def __init__(self, 
                 configs: Configs = None, 
                 resources: dict[str, Callable] = None
                 ) -> None:
        self.configs = configs
        self.resources = resources

        self.reports_dir: Path = self.configs.reports_dir
        self.collectors: list[Collector] = self.resources["collectors"]
        self._validate_collector_attributes()


    def _validate_collector_attributes(self) -> None:
        """Check if the collectors have the required attributes."""
        for collector in self.collectors:
            # Check if collector has the following attributes
            attrs = [
                "name", "results", "run", "generate_markdown_report"
            ]
            for attr in attrs:
                if not hasattr(collector, attr):
                    raise AttributeError(f"Collector {collector} does not have '{attr}' attribute")

            # Check if results attribute has the following attributes
            attrs = [
                "errors", "to_dict"
            ]
            for attr in attrs:
                if not hasattr(collector.results, attr):
                    raise AttributeError(f"Collector {collector} results does not have '{attr}' attribute")


    def _generate_reports(self, collector: Any) -> None:
        """
        Generate both JSON and Markdown reports of the linting results.
        """
        name = collector.name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        paths = [
            f"{name}_report_{timestamp}.json",
            f"{name}_report_{timestamp}.md",
            f"latest_{name}_report.json",
            f"latest_{name}_report.md"
        ]

        for path in paths:
            path = self.reports_dir / path
            match path.suffix:
                case ".json":
                    with open(path, 'w') as f:
                        json.dump(collector.results.to_dict(), f, indent=2)
                case ".md":
                    # Write the markdown file
                    with open(path, 'w') as f:
                        f.write('\n'.join(collector.generate_markdown_report()))
                case _:
                    raise ValueError(f"Unsupported file type: {path.suffix}")

        logger.info(f"\n{name} reports generated in {self.reports_dir}:")
        for path in paths:
            logger.info(f"{self.reports_dir / path}")


    def run(self) -> int:
        """
        Run the specified tests and generate reports.
        """
        for collector in self.collectors:
            name = collector.name

            logger.info(f"\n==== Running {name} ====")

            tests_were_successful = collector.run()

            if tests_were_successful:
                logger.info(f"\n✅ All {name} tests passed!")
            else:
                logger.info(f"\n❌ Tests {name} failed with {collector.results.errors} errors and {collector.results.failures} failures.")

            self._generate_reports(collector)

# results.py
from dataclasses import dataclass, field
from datetime import datetime

# We need a results class for each collector
@dataclass
class Results:
    """Test results class for collecting test/lint outputs."""

    name: str = "base"
    errors: int = 0
    failures: int = 0
    tests: int = 0
    status: str = "not_run"
    test_cases: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration: int = 0
    success_rate: int = 0
    skipped: int = 0
    expected_failures: int = 0
    unexpected_successes: int = 0

    def to_dict(self):
        """Convert results to a dictionary."""
        return {
            "summary": {
                "name": self.name,
                "errors": self.errors,
                "failures": self.failures,
                "tests": self.tests,
                "status": self.status,
                "timestamp": self.timestamp,
                "duration": self.duration,
                "success_rate": self.success_rate
            },
            "details": {
                "test_cases": self.test_cases,
                "issues": self.issues
            }
        }

def create_results(name: str) -> Results:
    """Factory function for creating result objects."""
    results = Results()
    results.name = name
    return results

def main() -> None:
    """
    Main entry point for the CLI.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run tests, type checking, and linting for a specified Python project."
    )
    parser.add_argument("--path", required=True, type=str, default=".", 
                        help="Path to the project directory")
    parser.add_argument("-q", "--quiet", action="store_true", 
                        help="Run tests with reduced verbosity")
    parser.add_argument("--mypy", action="store_true", 
                        help="Run mypy type checking")
    parser.add_argument("--flake8", action="store_true", 
                        help="Run flake8 linting")
    parser.add_argument("--corner-cutting", action="store_true", 
                        help="""Run corner cutting checks.
                        Corner cutting is defined as implementation shortcuts, temporary solutions, or placeholders 
                        that are likely to need improvement or replacement in the future.
                        """)
    parser.add_argument("--check-all", action="store_true", 
                        help="Run tests, type checking, linting, and corner cutting checks")
    parser.add_argument("--lint-only", action="store_true", 
                        help="Run only type checking and linting (no tests)")
    parser.add_argument("--respect-gitignore", "--gitignore", action="store_true",
                       help="Ignore files/folders listed in .gitignore during linting")
    
    args = parser.parse_args()

    # Determine what to run
    project_path = Path(args.path).resolve()
    run_tests = not args.lint_only
    run_mypy = args.mypy or args.check_all or args.lint_only
    run_flake8 = args.flake8 or args.check_all or args.lint_only
    run_corner_cutting = args.corner_cutting or args.check_all

    # Set the configs for the test runner
    configs = Configs(
        test_dir=project_path / "tests",
        reports_dir=project_path / "test_reports",
        respect_gitignore=args.respect_gitignore,
        verbosity=1 if args.quiet else 2
    )


        
    # Run the tests if requested
    resources = {
        "collectors": []
    }
    if run_tests: # Unit tests with unittest
        unittest_resources = {
            "name": "unittest",
            "create_results": create_results,
            "run_command": unittest_run_command,
            "parse_output": unittest_parse_output,
            "format_report": unittest_format_report
        }
        resources["collectors"].append(Collector(configs=configs, resources=unittest_resources))
        
    if run_mypy: # Type checking
        mypy_resources = {
            "name": "mypy",
            "create_results": create_results,
            "run_command": mypy_run_command,
            "parse_output": mypy_parse_output,
            "format_report": mypy_format_report
        }
        resources["collectors"].append(Collector(configs=configs, resources=mypy_resources))
        
    if run_flake8: # Code style
        flake8_resources = {
            "name": "flake8",
            "create_results": create_results,
            "run_command": flake8_run_command,
            "parse_output": flake8_parse_output,
            "format_report": flake8_format_report
        }
        resources["collectors"].append(Collector(configs=configs, resources=flake8_resources))
        
    if run_corner_cutting: # LLM laziness
        corner_cutting_resources = {
            "name": "corner_cutting",
            "create_results": create_results,
            "run_command": corner_cutting_run_command,
            "parse_output": corner_cutting_parse_output,
            "format_report": corner_cutting_format_report
        }
        resources["collectors"].append(Collector(configs=configs, resources=corner_cutting_resources))
    
    # Show usage help if nothing was run
    if not run_tests and not run_mypy and not run_flake8 and not run_corner_cutting:
        parser.print_help()

    # Run the tests and save their results
    try:
        runner = RunTestsAndSaveTheirResults(configs, resources)
        runner.run()
        logger.info("\n==== All tests completed ====")
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("\n\nKeyboard interrupt detected. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
