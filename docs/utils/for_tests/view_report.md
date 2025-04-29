# view_report.py: last updated 03:33 PM on April 27, 2025

**File Path:** `run_tests_and_save_their_results/utils/for_tests/view_report.py`

## Module Description

Simple viewer for test reports.

## Table of Contents

### Functions

- [`print_color`](#print_color)
- [`view_report`](#view_report)
- [`_display_json_report`](#_display_json_report)
- [`_display_markdown_report`](#_display_markdown_report)
- [`main`](#main)

## Functions

## `print_color`

```python
def print_color(text, color=None)
```

Print colored text to the console.

**Parameters:**

- `text` (`str`): The text to print

- `color` (`Optional[str]`): Optional color name ('red', 'green', etc.)

## `view_report`

```python
def view_report(report_path, format_type='summary')
```

View a test report file.

**Parameters:**

- `report_path` (`Union[(str, Path)]`): Path to the report file

- `format_type` (`str`): Type of report to show (summary, details, full)

**Returns:**

- `bool`: True if report was displayed successfully, False otherwise

## `_display_json_report`

```python
def _display_json_report(report, format_type)
```

Display a JSON report.

**Parameters:**

- `report` (`Dict[(str, Any)]`): The parsed JSON report

- `format_type` (`str`): Format type (summary, details, full)

## `_display_markdown_report`

```python
def _display_markdown_report(report_path)
```

Display a Markdown report.

**Parameters:**

- `report_path` (`Path`): Path to the Markdown report file

## `main`

```python
def main()
```

Main entry point.
