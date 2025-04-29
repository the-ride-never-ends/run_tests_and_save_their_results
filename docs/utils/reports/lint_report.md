# lint_report.py: last updated 03:33 PM on April 27, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/lint_report.py`

## Module Description

Script to generate reports for mypy and flake8 linting.

## Table of Contents

### Functions

- [`run_linting`](#run_linting)

### Classes

- [`LintResultCollector`](#lintresultcollector)

## Functions

## `run_linting`

```python
def run_linting(respect_gitignore=False)
```

Run linting and generate reports.

**Parameters:**

- `respect_gitignore` (`bool`): Whether to respect gitignore patterns

**Returns:**

- `Tuple[(bool, Dict[(str, Any)])]`: Tuple of success status and lint results dictionary

## Classes

## `LintResultCollector`

```python
class LintResultCollector(object)
```

Collects and formats linting results for reporting.

**Methods:**

- [`collect_flake8_results`](#collect_flake8_results)
- [`collect_mypy_results`](#collect_mypy_results)
- [`generate_json_report`](#generate_json_report)
- [`generate_markdown_report`](#generate_markdown_report)
- [`update_overall_status`](#update_overall_status)

### `collect_flake8_results`

```python
def collect_flake8_results(self, output)
```

Collect results from flake8 output.

**Parameters:**

- `output` (`str`): Output from flake8 command

**Returns:**

- `Tuple[(bool, int)]`: Tuple of success status and error count

### `collect_mypy_results`

```python
def collect_mypy_results(self, output)
```

Collect results from mypy output.

**Parameters:**

- `output` (`str`): Output from mypy command

**Returns:**

- `Tuple[(bool, int)]`: Tuple of success status and error count

### `generate_json_report`

```python
def generate_json_report(self, output_path)
```

Generate a JSON report of the linting results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

### `generate_markdown_report`

```python
def generate_markdown_report(self, output_path)
```

Generate a Markdown report of the linting results.

**Parameters:**

- `output_path` (`Path`): Path to write the report to

### `update_overall_status`

```python
def update_overall_status(self)
```

Update the overall status based on mypy and flake8 statuses.
