# run_command.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/flake8/run_command.py`

## Module Description

Utility function to run flake8 linting.

## Table of Contents

### Functions

- [`run_command`](#run_command)

## Functions

## `run_command`

```python
def run_command(configs)
```

Run flake8 linting and return the output.

**Parameters:**

- `configs` (`Dict[(str, Any)]`): Configuration dictionary with linting settings

**Returns:**

- `str`: The output from flake8

**Raises:**

- `RuntimeError`: If there's an error running flake8
