# unittest_.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/reports/services/unittest_.py`

## Module Description

Run unittest tests for Test Generator tool, then save the results to json and markdown.
Uses inversion of control with dependency injection for better testability.

## Table of Contents

### Classes

- [`UnittestCollector`](#unittestcollector)

## Classes

## `UnittestCollector`

```python
class UnittestCollector(Collector)
```

Discovers and runs unit tests, then generates reports using dependency injection.

**Constructor Parameters:**

- `configs` (`Any`): Configuration dataclass
- `resources` (`Any`): Dictionary of resources used by the collector

**Methods:**

