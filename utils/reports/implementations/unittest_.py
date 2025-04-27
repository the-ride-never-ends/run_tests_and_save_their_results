"""
Run unittest tests for Test Generator tool, then save the results to json and markdown.
"""
from datetime import datetime
import time
from typing import Any, Dict, List
import unittest


from utils.common.results import Results


class UnittestCollector:
    """Discovers and runs tests, then generates reports."""

    def __init__(self):
        """Initialize the collector with a start time."""
        self.name = "unittest"
        self.start_time = time.time()
        self.results: Results = Results(name=self.name)

    def collect_results(self, result: unittest.TestResult) -> None:
        """
        Collect results from a TestResult object.

        Args:
            result: TestResult object from the test run
        """
        # Calculate duration
        duration = time.time() - self.start_time

        # Initialize test cases list
        test_cases_list: List[Dict[str, Any]] = []

        # Update results object attributes
        self.results.tests = result.testsRun
        self.results.errors = len(result.errors)
        self.results.failures = len(result.failures)
        self.results.skipped = len(result.skipped)
        self.results.expected_failures = len(getattr(result, 'expectedFailures', []))
        self.results.unexpected_successes = len(getattr(result, 'unexpectedSuccesses', []))

        # Calculate success rate
        success_count = result.testsRun - len(result.errors) - len(result.failures)
        self.results.success_rate = (success_count / result.testsRun) * 100 if result.testsRun > 0 else 0
        self.results.duration = round(duration, 2)

        # Process failures
        for test, traceback in result.failures:
            test_cases_list.append({
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
            test_cases_list.append({
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
            test_cases_list.append({
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
            test_cases_list.append({
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
            test_cases_list.append({
                "id": str(test.id()),
                "name": test._testMethodName,
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "status": "UNEXPECTED_SUCCESS",
                "message": "Test unexpectedly passed",
                "traceback": ""
            })

        # Update the results object with test cases
        self.results.test_cases = test_cases_list


    def _extract_message(self, traceback: str) -> str:
        """Extract the error message from a traceback."""
        lines = traceback.strip().split('\n')
        return lines[-1] if lines else "No message"


    def generate_markdown_report(self) -> str:
        """
        Generate a Markdown report of the test results.
        """
        # Format timestamp
        timestamp = datetime.fromisoformat(self.results.timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # Build markdown content
        content: List[str] = [
            "# Test Generator - Test Report",
            f"Generated on: {timestamp}\n",
            "## Summary",
            f"- **Tests Run**: {self.results.tests}",
            f"- **Passed**: {self.results.tests - self.results.failures - self.results.errors}",
            f"- **Failures**: {self.results.failures}",
            f"- **Errors**: {self.results.errors}",
            f"- **Skipped**: {self.results.skipped}",
            f"- **Expected Failures**: {self.results.expected_failures}",
            f"- **Unexpected Successes**: {self.results.unexpected_successes}",
            f"- **Success Rate**: {self.results.success_rate:.2f}%",
            f"- **Duration**: {self.results.duration} seconds",
            "",
        ]

        # Add test details if there are any issues
        if self.results.test_cases:
            content.extend([
                "## Test Details\n",
                "| Status | Module | Class | Test |",
                "|--------|--------|-------|------|",
            ])

            for test_case in self.results.test_cases:
                status = str(test_case.get("status", ""))
                module = str(test_case.get("module", ""))
                cls = str(test_case.get("class", ""))
                name = str(test_case.get("name", ""))

                content.append(f"| {status} | {module} | {cls} | {name} |")

            # Add failure/error details
            failures_or_errors = [tc for tc in self.results.test_cases if tc.get("status") in ("FAIL", "ERROR")]
            if failures_or_errors:
                content.append("\n## Failure and Error Details\n")

                for tc in failures_or_errors:
                    tc_status = str(tc.get("status", ""))
                    tc_module = str(tc.get("module", ""))
                    tc_class = str(tc.get("class", ""))
                    tc_name = str(tc.get("name", ""))
                    tc_message = str(tc.get("message", ""))
                    tc_traceback = str(tc.get("traceback", ""))

                    content.extend([
                        f"### {tc_status}: {tc_module}.{tc_class}.{tc_name}",
                        f"**Message**: {tc_message}",
                        f"```\n{tc_traceback}\n```\n",
                    ])
        return content

    def run(self, configs) -> bool:
        """
        Run the test suite and collect results.

        Args:
            configs: Configuration dataclass
        Returns:
            bool: True if all tests passed, False otherwise
        """
        # Run the test suite
        test_suite = unittest.defaultTestLoader.discover(str(configs.test_dir))
        test_runner = unittest.TextTestRunner(verbosity=configs.verbosity)
        result = test_runner.run(test_suite)

        # Collect results
        self.collect_results(result)

        return result.wasSuccessful()
