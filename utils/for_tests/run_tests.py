#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to run all tests for Test Generator and generate reports.
"""
import datetime
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple, Any, List, cast
import unittest


class TestResultCollector:
    """Collects and formats test results for reporting."""

    def __init__(self):
        """Initialize the collector with a start time."""
        self.start_time = time.time()
        self.results: Dict[str, Any] = {
            "summary": {
                "tests": 0,
                "errors": 0,
                "failures": 0,
                "skipped": 0,
                "expected_failures": 0,
                "unexpected_successes": 0,
                "success_rate": 0.0,
                "duration": 0.0,
                "timestamp": datetime.datetime.now().isoformat(),
            },
            "test_cases": []
        }

    def collect_results(self, result: unittest.TestResult) -> None:
        """
        Collect results from a TestResult object.

        Args:
            result: TestResult object from the test run
        """
        # Calculate duration
        duration = time.time() - self.start_time

        # Get the summary dict
        summary = cast(Dict[str, Any], self.results["summary"])
        test_cases = cast(List[Dict[str, Any]], self.results["test_cases"])

        # Update summary
        summary["tests"] = result.testsRun
        summary["errors"] = len(result.errors)
        summary["failures"] = len(result.failures)
        summary["skipped"] = len(result.skipped)
        summary["expected_failures"] = len(getattr(result, 'expectedFailures', []))
        summary["unexpected_successes"] = len(getattr(result, 'unexpectedSuccesses', []))

        # Calculate success rate
        success_count = result.testsRun - len(result.errors) - len(result.failures)
        summary["success_rate"] = (success_count / result.testsRun) * 100 if result.testsRun > 0 else 0
        summary["duration"] = round(duration, 2)

        # Process failures
        for test, traceback in result.failures:
            test_cases.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "FAIL",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process errors
        for test, traceback in result.errors:
            test_cases.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "ERROR",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process skipped tests
        for test, reason in result.skipped:
            test_cases.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "SKIPPED",
                "message": reason,
                "traceback": ""
            })

        # Process expected failures
        for test, traceback in getattr(result, 'expectedFailures', []):
            test_cases.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "EXPECTED_FAILURE",
                "message": self._extract_message(traceback),
                "traceback": traceback
            })

        # Process unexpected successes
        for test in getattr(result, 'unexpectedSuccesses', []):
            test_cases.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "UNEXPECTED_SUCCESS",
                "message": "Test unexpectedly passed",
                "traceback": ""
            })

    def _extract_message(self, traceback: str) -> str:
        """Extract the error message from a traceback."""
        lines = traceback.strip().split('\n')
        return lines[-1] if lines else "No message"

    def generate_json_report(self, output_path: Path) -> None:
        """
        Generate a JSON report of the test results.

        Args:
            output_path: Path to write the report to
        """
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

    def generate_markdown_report(self, output_path: Path) -> None:
        """
        Generate a Markdown report of the test results.

        Args:
            output_path: Path to write the report to
        """
        summary_dict = cast(Dict[str, Any], self.results["summary"])
        test_cases_list = cast(List[Dict[str, Any]], self.results["test_cases"])

        # Format timestamp
        timestamp = datetime.datetime.fromisoformat(str(summary_dict["timestamp"]))
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Build markdown content
        content: List[str] = [
            "# Test Generator - Test Report",
            f"Generated on: {formatted_time}",
            "",
            "## Summary",
            "",
            f"- **Tests Run**: {summary_dict['tests']}",
            f"- **Passed**: {summary_dict['tests'] - summary_dict['failures'] - summary_dict['errors']}",
            f"- **Failures**: {summary_dict['failures']}",
            f"- **Errors**: {summary_dict['errors']}",
            f"- **Skipped**: {summary_dict['skipped']}",
            f"- **Expected Failures**: {summary_dict['expected_failures']}",
            f"- **Unexpected Successes**: {summary_dict['unexpected_successes']}",
            f"- **Success Rate**: {summary_dict['success_rate']:.2f}%",
            f"- **Duration**: {summary_dict['duration']} seconds",
            "",
        ]

        # Add test details if there are any issues
        if test_cases_list:
            content.extend([
                "## Test Details",
                "",
                "| Status | Module | Class | Test |",
                "|--------|--------|-------|------|",
            ])

            for test_case in test_cases_list:
                status = str(test_case.get("status", ""))
                module = str(test_case.get("module", ""))
                cls = str(test_case.get("class", ""))
                name = str(test_case.get("name", ""))

                content.append(f"| {status} | {module} | {cls} | {name} |")

            # Add failure/error details
            failures_or_errors = [tc for tc in test_cases_list if tc.get("status") in ("FAIL", "ERROR")]
            if failures_or_errors:
                content.extend([
                    "",
                    "## Failure and Error Details",
                    ""
                ])

                for tc in failures_or_errors:
                    tc_status = str(tc.get("status", ""))
                    tc_module = str(tc.get("module", ""))
                    tc_class = str(tc.get("class", ""))
                    tc_name = str(tc.get("name", ""))
                    tc_message = str(tc.get("message", ""))
                    tc_traceback = str(tc.get("traceback", ""))

                    content.extend([
                        f"### {tc_status}: {tc_module}.{tc_class}.{tc_name}",
                        "",
                        f"**Message**: {tc_message}",
                        "",
                        "```",
                        tc_traceback,
                        "```",
                        ""
                    ])

        # Write the markdown file
        with open(output_path, 'w') as f:
            f.write('\n'.join(content))


class RunTests:
    """Discovers and runs tests, then generates reports."""

    def __init__(self, test_dir: Path, reports_dir: Path, verbosity: int = 2):
        """
        Initialize the test runner.

        Args:
            test_dir: Directory to look for tests in
            verbosity: Verbosity level for test output
        """
        self.test_dir = test_dir
        self.reports_dir = reports_dir
        self.verbosity = verbosity

    def run(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Discover and run tests, then return the results.

        Returns:
            Tuple containing success status and test results
        """
        # Discover tests
        test_suite = unittest.defaultTestLoader.discover(str(self.test_dir))

        # Create result collector
        collector = TestResultCollector()

        # Run tests
        test_runner = unittest.TextTestRunner(verbosity=self.verbosity)
        result = test_runner.run(test_suite)

        # Collect results
        collector.collect_results(result)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        json_path = self.reports_dir / f"test_report_{timestamp}.json"
        markdown_path = self.reports_dir / f"test_report_{timestamp}.md"

        collector.generate_json_report(json_path)
        collector.generate_markdown_report(markdown_path)

        print("\nTest reports generated:")
        print(f"  - JSON: {json_path}")
        print(f"  - Markdown: {markdown_path}")

        # Also generate latest report links
        latest_json = self.reports_dir / "latest_test_report.json"
        latest_md = self.reports_dir / "latest_test_report.md"

        collector.generate_json_report(latest_json)
        collector.generate_markdown_report(latest_md)

        return result.wasSuccessful(), collector.results


if __name__ == "__main__":
    # Set verbosity from command line arguments
    verbosity = 2
    if len(sys.argv) > 1 and sys.argv[1] == "-q":
        verbosity = 1

    # Discover and run tests
    # Use the current working directory (which should be the project root due to cd in run.sh)
    test_dir = Path.cwd() / "tests"
    print(f"Looking for tests in: {test_dir}")
    runner = RunTests(test_dir, verbosity)

    success, _ = runner.run()

    # Exit with non-zero code if tests failed
    sys.exit(0 if success else 1)
