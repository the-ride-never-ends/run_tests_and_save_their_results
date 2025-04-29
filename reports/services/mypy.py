"""
Generate reports for type checking with mypy.
"""
from datetime import datetime
import subprocess
from typing import Dict, Any, List, Tuple


from configs import Configs
from utils.common.results import Results
from utils.common.should_ignore_file import should_ignore_file


class MyPyCollector:
    """Collects and formats linting results for reporting."""


    def __init__(self) -> None:
        """Initialize the collector."""
        self.name = "mypy"
        self.results: Results = Results(name=self.name)


    def collect_results(self, output: str) -> Tuple[bool, int]:
        """
        Collect results from mypy output.

        Args:
            output: Output from mypy command

        Returns:
            Tuple of success status and error count
        """
        # Parse mypy output
        lines = output.strip().split('\n')
        error_count = 0

        for line in lines:
            if not line or "Success: no issues found" in line:
                continue

            error_count += 1

            # Try to parse the error line
            try:
                # Format is typically: file:line: error: message  [error-code]
                parts = line.split(':', 3)

                if len(parts) >= 3:
                    file_path = parts[0]
                    line_num = parts[1]
                    message = parts[2:]

                    # Join the remaining parts as the message
                    message_text = ':'.join(message).strip()

                    # Extract error code if present
                    error_code = ""
                    if "[" in message_text and "]" in message_text:
                        error_code = message_text.split('[')[-1].split(']')[0]

                    self.results.issues.append({
                        "file": file_path,
                        "line": line_num,
                        "message": message_text,
                        "error_code": error_code
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

        # Return success status and error count
        return error_count == 0, error_count


    def generate_markdown_report(self) -> None:
        """
        Generate a Markdown report of the linting results.

        Args:
            output_path: Path to write the report to
        """
        # Format timestamp
        timestamp = datetime.fromisoformat(self.results.timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # Build markdown content
        content: List[str] = [
            "# Type Check Report - mypy\n",
            f"Generated on: {timestamp}\n",
            "## Summary\n",
            f"- **Type Checking (mypy)**: {self.results.status.upper()} ({self.results.errors} issues)\n",
        ]

        # Add mypy issues
        if self.results.issues:
            content.append("## Type Checking Issues (mypy)\n")

            # Group issues by file
            file_issues: Dict[str, List[Dict[str, Any]]] = {}
            for issue in self.results.issues:
                file_path = issue.get("file", "Unknown file")
                if file_path not in file_issues:
                    file_issues[file_path] = []
                file_issues[file_path].append(issue)

            # Add issues by file
            for file_path, issues in file_issues.items():
                content.append(f"### {file_path}\n")

                for issue in issues:
                    line = issue.get("line", "")
                    message = issue.get("message", "")
                    error_code = issue.get("error_code", "")

                    error_info = f"Line {line}: {message}"
                    if error_code:
                        error_info += f" [{error_code}]"

                    content.append(f"- {error_info}")
                content.append("")


    def run(self, configs: Configs) -> bool:
        """
        Run mypy type checking on the project and collect results.

        If respect_gitignore is True and gitignore_spec is provided, issues in git-ignored
        files are filtered out.

        Args:
            respect_gitignore: Boolean indicating whether to ignore issues in gitignored files.
            gitignore_spec: Specification of gitignored files, used if respect_gitignore is True.

        Returns:
            bool: True if type checking passed with no errors, False otherwise.

        Raises:
            Exception: If mypy fails to run.
        """
        print("Running mypy type checking...")
        cmd = ["mypy", "--config-file", "mypy.ini", "."]

        try:
            # Run mypy and capture the output
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
            print(f"Error running mypy: {e}")
            success = False
        return success
