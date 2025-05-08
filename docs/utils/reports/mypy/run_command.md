# run_command.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/mypy/run_command.py`

## Module Description

Utility function to run mypy type checking.

## Table of Contents

### Functions

- [`run_command`](#run_command)

## Functions

## `run_command`

```python
def run_command(configs)
```

Run mypy type checking and return the output.

**Parameters:**

- `configs` (`Dict[(str, Any)]`): Configuration dictionary with type checking settings

**Returns:**

- `str`: The output from mypy

**Raises:**

- `RuntimeError`: If there's an error running mypy
