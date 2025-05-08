# run_command.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/unittest/run_command.py`

## Module Description

Utility function to run unittest tests through subprocess.

## Table of Contents

### Functions

- [`run_command`](#run_command)

## Functions

## `run_command`

```python
def run_command(configs)
```

Run the unittest tests using a subprocess call to bash script.

**Parameters:**

- `configs` (`Dict[(str, Any)]`): Configuration dictionary with test_dir and other settings

**Returns:**

- `Any`: The result of running the tests

**Raises:**

- `ValueError`: If the operating system is not supported
RuntimeError: If the subprocess command fails
