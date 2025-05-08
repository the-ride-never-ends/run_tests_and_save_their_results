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

from reports.services.flake8 import Flake8Collector
from reports.services.mypy import MyPyCollector
from reports.services.unittest_ import UnittestCollector
from reports.services.corner_cutting import CornerCuttingCollector
from utils.main.show_report import show_report


class RunTestsAndSaveTheirResults:


    def __init__(self, configs: dict[str, Any] = None, resources: dict[str, Callable] = None) -> None:
        self.configs = configs
        self.resources = resources

        self.reports_dir: Path = self.configs.reports_dir
        self.collectors: list[Any] = self.resources["collectors"]
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
            logger.info(f"  - {path}")


    def run(self) -> int:
        """
        Run the specified tests and generate reports.
        """
        for collector in self.collectors:
            name = collector.name

            logger.info(f"\n==== Running {name} ====")

            tests_were_successful = collector.run(self.configs)

            if tests_were_successful:
                logger.info(f"\n✅ All {name} tests passed!")
            else:
                logger.info(f"\n❌ Tests {name} failed with {collector.results.errors} errors.")

            self._generate_reports(collector)

            # Show the latest report
            # show_report(self.reports_dir / f"latest_{name}_report.md")


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
        resources["collectors"].append(UnittestCollector())
    if run_mypy: # Type checking
        resources["collectors"].append(MyPyCollector())
    if run_flake8: # Code style
        resources["collectors"].append(Flake8Collector())
    if run_corner_cutting: # LLM laziness
        resources["collectors"].append(CornerCuttingCollector())
    
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