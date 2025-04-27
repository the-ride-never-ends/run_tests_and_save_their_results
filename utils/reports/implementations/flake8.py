"""
Generate reports for code style linting with flake8.
"""
from datetime import datetime
import subprocess
from typing import Dict, Any, List


from utils.common.should_ignore_file import should_ignore_file
from utils.common.results import Results


class Flake8Collector:
    """Collects and formats code style results for reporting."""


    def __init__(self) -> None:
        """Initialize the collector."""
        self.name = "flake8"
        self.results: Results = Results(name=self.name)


    def collect_results(self, output: str) -> bool:
        """
        Collect results from flake8 output.

        Args:
            output: Output from flake8 command

        Returns:
            Tuple of success status and error count
        """
        # Parse flake8 output
        error_count = 0

        for line in output.strip().split('\n'):
            if not line:
                continue

            error_count += 1

            # Try to parse the error line
            try:
                # Format is typically: ./file.py:line:col: code message
                parts = line.split(':', 3)

                if len(parts) >= 4:
                    file_path = parts[0]
                    line_num = parts[1]
                    col_num = parts[2]
                    code_message = parts[3].strip().split(' ', 1)

                    self.results.issues.append({
                        "file": file_path,
                        "line": line_num,
                        "column": col_num,
                        "error_code": code_message[0] if len(code_message) > 0 else "",
                        "message": code_message[1] if len(code_message) > 1 else ""
                    })
                else:
                    # If we can't parse it, just add the whole line
                    self.results.issues.append({
                        "message": line
                    })
            except Exception:
                # If any parsing error, just add the whole line
                self.results.issues.append({
                    "message": line
                })

        # Update summary
        self.results.errors = error_count
        self.results.status = "pass" if error_count == 0 else "fail"

        return error_count == 0


    def generate_markdown_report(self) -> None:
        """
        Generate a Markdown report of the linting results.

        Args:
            output_path: Path to write the report to
        """
        timestamp = datetime.fromisoformat(self.results.timestamp)

        # Build markdown content
        content: List[str] = [
            "# Code Style Report - flake8\n",
            f"Generated on: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n",
            "## Summary\n",
            f"- **Code Style (flake8)**: {self.results.status.upper()} ({self.results.errors} issues)\n",
        ]

        # Add flake8 issues
        if self.results.issues:
            content.append("## Code Style Issues (flake8)\n")

            # Group issues by file
            files_with_issues: Dict[str, List[Dict[str, Any]]] = {}
            for issue in self.results.issues:
                file_path = issue.get("file", "Unknown file")
                if file_path not in files_with_issues:
                    files_with_issues[file_path] = []
                files_with_issues[file_path].append(issue)

            # Add issues by file
            for file_path, issues in files_with_issues.items():
                content.append(f"### {file_path}\n\n")

                for issue in issues:
                    line = issue.get("line", "")
                    column = issue.get("column", "")
                    message = issue.get("message", "")
                    error_code = issue.get("error_code", "")

                    location = f"Line {line}"
                    if column:
                        location += f", Col {column}"

                    content.append(f"- {location}: {error_code} {message}")

                content.append("")


    def run(self, configs) -> tuple[bool, Any]:
        """Run flake8 linting on the codebase and process the results.

        If `respect_gitignore` is True, issues from files
        listed in .gitignore are filtered out.

        Args:
            collector: A collector object that processes and stores test results.
            respect_gitignore (bool): Whether to ignore issues from files in .gitignore.
            gitignore_spec: The parsed gitignore specifications used for filtering.

        Returns:
            bool: True if flake8 linting passed (no errors), False otherwise.

        Raises:
            Exception: If there's an error running flake8.
        """
        cmd = ["flake8"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            success = self.collect_results(result.stdout + result.stderr)

            if configs.respect_gitignore and configs.gitignore_spec:
                # Filter out issues in ignored files
                filtered_issues = []
                filtered_count = 0
                for issue in self.results.issues:
                    file_path = issue.get("file", "")
                    if file_path and should_ignore_file(file_path, configs.gitignore_spec):
                        filtered_count += 1
                    else:
                        filtered_issues.append(issue)

                if filtered_count > 0:
                    print(f"Ignored {filtered_count} issues in gitignored files")
                    self.results.issues = filtered_issues
                    self.results.errors -= filtered_count
                    success = self.results.errors == 0

        except Exception as e:
            print(f"Error running flake8: {e}")
            success = False
        return success
