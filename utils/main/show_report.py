from pathlib import Path
import subprocess


from logger import logger


def _find_markdown_viewer() -> tuple[str, str]:
    """
    Find an available markdown viewer.

    Returns:
        Tuple with command and its description
    """
    command_type = ["glow", "bat", "less"]
    for cmd in command_type:
        cmd_list = ["command", "-v", cmd]
        _cmd = ' '.join(cmd_list)
        if subprocess.run(_cmd, shell=True, capture_output=True).returncode == 0:
            logger.debug(f"Found {cmd} command")
            match cmd:
                case "glow" | "bat":
                    return _cmd, "Showing report preview:"
                case "less":
                    return _cmd, "Showing report preview (press q to exit):"
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
        output = subprocess.run([viewer_cmd, " ", report_path.resolve()], shell=True, capture_output=True)
        print(output.stdout.decode("utf-8"))
    else:
        print(f"\n{description}")
