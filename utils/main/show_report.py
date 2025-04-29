from pathlib import Path
import subprocess


def _find_markdown_viewer() -> tuple[str, str]:
    """
    Find an available markdown viewer.

    Returns:
        Tuple with command and its description
    """
    command_type = ["glow", "bat", "less"]
    for cmd in command_type:
        if subprocess.run(["command", "-v", cmd], shell=True, capture_output=True).returncode == 0:
            match cmd:
                case "glow" | "bat":
                    return cmd, "Showing report preview:"
                case "less":
                    return cmd, "Showing report preview (press q to exit):"
                case _:
                    return "", "To view the full report, open the file in a text editor."


def show_report(report_path: Path) -> None:
    """
    Show a report using the available viewer.

    Args:
        report_path: Path to the report file
    """
    if not report_path.exists():
        return

    print(f"\nLatest report is available at: {report_path}")

    # Check if the viewer command is available
    viewer_cmd, description = _find_markdown_viewer()

    if viewer_cmd:
        print(f"\n{description}")
        subprocess.run([viewer_cmd, str(report_path)])
    else:
        print(f"\n{description}")
