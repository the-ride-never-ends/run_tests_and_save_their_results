# logger.py: last updated 08:02 PM on May 07, 2025

**File Path:** `run_tests_and_save_their_results/logger.py`

## Table of Contents

### Functions

- [`get_logger`](#get_logger)

## Functions

## `get_logger`

```python
def get_logger(name, log_file_name='app.log', level=logging.INFO, max_size=5 * 1024 * 1024, backup_count=3)
```

Sets up a logger with both file and console handlers.

**Parameters:**

- `name` (`str`): Name of the logger.

- `log_file_name` (`str`): Name of the log file. Defaults to 'app.log'.

- `level` (`int`): Logging level. Defaults to logging.INFO.

- `max_size` (`int`): Maximum size of the log file before it rotates. Defaults to 5MB.

- `backup_count` (`int`): Number of backup files to keep. Defaults to 3.

**Returns:**

- `logging.Logger`: Configured logger.

**Examples:**

```python
# Usage
    logger = get_logger(__name__)
```
