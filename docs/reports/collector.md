# collector.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/reports/collector.py`

## Module Description

Base collector interface for running tests and generating reports.
Using inversion of control pattern for configuration and resource management.

## Table of Contents

### Classes

- [`Collector`](#collector)

## Classes

## `Collector`

```python
class Collector(object)
```

Base collector class for test runners and report generators.
Implements the inversion of control pattern for better testability and flexibility.

**Constructor Parameters:**

- `configs` (`Any`): Configuration dataclass
- `resources` (`Any`): Dictionary of resources used by the collector

**Methods:**

- [`generate_markdown_report`](#generate_markdown_report)
- [`run`](#run)

### `generate_markdown_report`

```python
def generate_markdown_report(self)
```

Generate a Markdown report of the results.

**Returns:**

- `List[str]`: Lines of the markdown report

### `run`

```python
def run(self)
```

Run the test/linting command and collect results.

**Returns:**

- `bool`: True if successful, False otherwise
