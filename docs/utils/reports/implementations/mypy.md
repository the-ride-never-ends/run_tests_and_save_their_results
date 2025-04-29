# mypy.py: last updated 03:33 PM on April 27, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/implementations/mypy.py`

## Module Description

Generate reports for type checking with mypy.

## Table of Contents

### Classes

- [`MyPyCollector`](#mypycollector)

## Classes

## `MyPyCollector`

```python
class MyPyCollector(object)
```

Collects and formats linting results for reporting.

**Methods:**

- [`collect_results`](#collect_results)
- [`generate_markdown_report`](#generate_markdown_report)
- [`run`](#run)

### `collect_results`

```python
def collect_results(self, output)
```

Collect results from mypy output.

**Parameters:**

- `output` (`str`): Output from mypy command

**Returns:**

- `Tuple[(bool, int)]`: Tuple of success status and error count

### `generate_markdown_report`

```python
def generate_markdown_report(self)
```

Generate a Markdown report of the linting results.

**Parameters:**

- `output_path` (`Any`): Path to write the report to

### `run`

```python
def run(self, configs)
```

Run mypy type checking on the project and collect results.

If respect_gitignore is True and gitignore_spec is provided, issues in git-ignored
files are filtered out.

**Parameters:**

- `respect_gitignore` (`Any`): Boolean indicating whether to ignore issues in gitignored files.

- `gitignore_spec` (`Any`): Specification of gitignored files, used if respect_gitignore is True.

**Returns:**

- `bool`: True if type checking passed with no errors, False otherwise.

**Raises:**

- `Exception`: If mypy fails to run.
