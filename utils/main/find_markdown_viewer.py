import subprocess


def find_markdown_viewer() -> tuple[str, str]:
    """
    Find an available markdown viewer.

    Returns:
        Tuple with command and its description
    """
    if subprocess.run(["command", "-v", "glow"], shell=True, capture_output=True).returncode == 0:
        return "glow", "Showing report preview:"
    elif subprocess.run(["command", "-v", "bat"], shell=True, capture_output=True).returncode == 0:
        return "bat", "Showing report preview:"
    elif subprocess.run(["command", "-v", "less"], shell=True, capture_output=True).returncode == 0:
        return "less", "Showing report preview (press q to exit):"
    else:
        return "", "To view the full report, open the file in a text editor."
