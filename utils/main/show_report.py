from pathlib import Path
import subprocess


def show_report(report_path: Path, viewer_cmd: str, description: str) -> None:
    """
    Show a report using the available viewer.

    Args:
        report_path: Path to the report file
        viewer_cmd: Command to use for viewing
        description: Description to show before the report
    """
    if not report_path.exists():
        return

    print(f"\nLatest report is available at: {report_path}")

    if viewer_cmd:
        print(f"\n{description}")
        subprocess.run([viewer_cmd, str(report_path)])
    else:
        print(f"\n{description}")
