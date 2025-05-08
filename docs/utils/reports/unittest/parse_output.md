# parse_output.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/unittest/parse_output.py`

## Module Description

Utility function to parse the output of unittest test runs.

## Table of Contents

### Functions

- [`parse_output`](#parse_output)
- [`_extract_test_failures`](#_extract_test_failures)

## Functions

## `parse_output`

```python
def parse_output(output, results)
```

Parse the output from the unittest run and populate the results object.

**Parameters:**

- `output` (`str`): String output from the unittest run

- `results` (`Any`): Results object to populate

**Returns:**

- `bool`: True if all tests passed, False otherwise

## `_extract_test_failures`

```python
def _extract_test_failures(output)
```

Extract individual test failures from unittest output.

**Parameters:**

- `output` (`str`): String output from unittest

**Returns:**

- `list`: List of test failure dictionaries
