#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple viewer for test reports.
"""
import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Union


def print_color(text: str, color: Optional[str] = None) -> None:
    """
    Print colored text to the console.

    Args:
        text: The text to print
        color: Optional color name ('red', 'green', etc.)
    """
    colors: Dict[str, str] = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "end": "\033[0m"
    }

    if not color or not sys.stdout.isatty():
        print(text)
    else:
        print(f"{colors.get(color, '')}{text}{colors['end']}")


def view_report(report_path: Union[str, Path], format_type: str = "summary") -> bool:
    """
    View a test report file.

    Args:
        report_path: Path to the report file
        format_type: Type of report to show (summary, details, full)

    Returns:
        bool: True if report was displayed successfully, False otherwise
    """
    report_path = Path(report_path)

    # Check if file exists
    if not report_path.exists():
        print_color(f"Error: Report file not found: {report_path}", "red")
        return False

    # Check file extension
    if report_path.suffix == ".json":
        # Parse JSON report
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                report: Dict[str, Any] = json.load(f)
        except json.JSONDecodeError as e:
            print_color(f"Error: Invalid JSON in report file: {e}", "red")
            return False

        # Display report
        _display_json_report(report, format_type)
    elif report_path.suffix == ".md":
        # Display Markdown report
        _display_markdown_report(report_path)
    else:
        print_color(f"Error: Unsupported report format: {report_path.suffix}", "red")
        return False

    return True


def _display_json_report(report: Dict[str, Any], format_type: str) -> None:
    """
    Display a JSON report.

    Args:
        report: The parsed JSON report
        format_type: Format type (summary, details, full)
    """
    summary: Dict[str, Any] = report["summary"]
    test_cases: List[Dict[str, Any]] = report["test_cases"]

    # Print summary header
    print_color("\n=== Test Generator - Test Report ===\n", "bold")

    # Print summary
    print_color("SUMMARY:", "bold")
    print(f"Tests Run:            {summary['tests']}")
    print(f"Passed:               {summary['tests'] - summary['failures'] - summary['errors']}")
    print(f"Failures:             {summary['failures']}")
    print(f"Errors:               {summary['errors']}")
    print(f"Skipped:              {summary['skipped']}")
    print(f"Expected Failures:    {summary['expected_failures']}")
    print(f"Unexpected Successes: {summary['unexpected_successes']}")

    success_rate: float = summary['success_rate']
    color: str = "green" if success_rate == 100 else "yellow" if success_rate >= 80 else "red"
    print("Success Rate:         ", end="")
    print_color(f"{success_rate:.2f}%", color)

    print(f"Duration:             {summary['duration']} seconds\n")

    # Print test case details if requested
    if format_type in ["details", "full"] and test_cases:
        print_color("TEST DETAILS:", "bold")

        # Group test cases by status
        cases_by_status: Dict[str, List[Dict[str, Any]]] = {}
        for case in test_cases:
            status = case["status"]
            if status not in cases_by_status:
                cases_by_status[status] = []
            cases_by_status[status].append(case)

        # Print cases by status
        for status, cases in cases_by_status.items():
            status_color = "red" if status in ["FAIL", "ERROR"] else "yellow" if status in ["SKIPPED", "EXPECTED_FAILURE"] else "green"
            print_color(f"\n{status} ({len(cases)}):", status_color)

            for case in cases:
                print(f"  {case['module']}.{case['class']}.{case['name']}")

                if format_type == "full":
                    print(f"    Message: {case['message']}")
                    if case["traceback"] and status in ["FAIL", "ERROR"]:
                        print("    Traceback:")
                        for line in case["traceback"].split("\n"):
                            print(f"      {line}")
                        print()


def _display_markdown_report(report_path: Path) -> None:
    """
    Display a Markdown report.

    Args:
        report_path: Path to the Markdown report file
    """
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content: str = f.read()

        # Very simple Markdown display
        lines: List[str] = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                print_color(line[2:], "bold")
            elif line.startswith("## "):
                print_color(f"\n{line[3:]}", "underline")
            elif line.startswith("### "):
                print_color(f"\n{line[4:]}", "bold")
            elif line.startswith("- **"):
                parts: List[str] = line.split("**")
                if len(parts) >= 3:
                    print(f"{parts[1]:<22} {parts[2][2:]}")
                else:
                    print(line)
            elif line.startswith("|"):
                # Simple table handling
                print(line)
            else:
                print(line)
    except Exception as e:
        print_color(f"Error displaying Markdown report: {e}", "red")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="View test reports for Test Generator.")
    parser.add_argument(
        "report_path",
        nargs="?",
        default="test_reports/latest_report.json",
        help="Path to the report file (default: test_reports/latest_report.json)"
    )
    parser.add_argument(
        "--format",
        choices=["summary", "details", "full"],
        default="summary",
        help="Format of the report output (default: summary)"
    )

    args = parser.parse_args()
    success = view_report(args.report_path, args.format)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
