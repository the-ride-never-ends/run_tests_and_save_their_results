# Test Runner and Report Generator

A standalone CLI utility for running tests, type checking, linting, and generating nicely formatted reports.

## Features

- Run unit tests and generate detailed JSON and Markdown reports
- Run type checking with mypy and generate reports of issues
- Run linting with flake8 and generate reports of issues
- Display reports using available tools (glow, bat, or less)
- Option to respect .gitignore patterns when linting
- Simple CLI with flexible options

## Usage

```bash
# Easy way: run with reporting
./run_tests.sh --path "path/to/program"

# Run type checking and linting
./run_tests.sh --path "path/to/program" --check-all          # Run tests + mypy + flake8
./run_tests.sh --path "path/to/program" --mypy               # Run tests + mypy type checking
./run_tests.sh --path "path/to/program" --flake8             # Run tests + flake8 linting
./run_tests.sh --path "path/to/program" --lint-only          # Only run mypy + flake8 (no tests)
./run_tests.sh --path "path/to/program" --respect-gitignore  # Ignore files/folders in .gitignore during linting

# You can combine options
./run_tests.sh --path "path/to/program" --lint-only --respect-gitignore  # Run linting only, respecting .gitignore
```

Or you can use the Python script directly:

```bash
python main.py --check-all
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Run the installation script
./install.sh
```

## Requirements

- Python 3.12+
- Dependencies listed in requirements.txt

## Project Structure

```
.
├── main.py                  # Main Python entry point
├── run_tests.sh             # Bash wrapper script
├── install.sh               # Installation script
├── requirements.txt         # Python dependencies
├── tests/                   # Directory for test files
└── utils/
    └── for_tests/
        ├── run_tests.py     # Test runner and report generator
        ├── lint_report.py   # Linting and type checking report generator
        ├── view_report.py   # Report viewer
        └── fix_whitespace.py # Whitespace issue fixer
```

## Reports

Reports are generated in the `test_reports` directory in both JSON and Markdown formats.