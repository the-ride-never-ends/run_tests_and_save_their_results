# load_gitignore_patterns_if_needed.py: last updated 03:33 PM on April 27, 2025

**File Path:** `run_tests_and_save_their_results/utils/common/load_gitignore_patterns_if_needed.py`

## Table of Contents

### Functions

- [`load_gitignore_patterns_if_needed`](#load_gitignore_patterns_if_needed)

## Functions

## `load_gitignore_patterns_if_needed`

```python
def load_gitignore_patterns_if_needed(respect_gitignore, reports_dir)
```

Load patterns from a .gitignore file if respect_gitignore is True.

This function reads patterns from a .gitignore file located in the parent directory
of reports_dir and constructs a PathSpec object that can be used to match paths
against these patterns.

**Parameters:**

- `respect_gitignore` (`bool`): Boolean indicating whether to respect .gitignore patterns.

- `reports_dir` (`Path`): Path object pointing to the reports directory.

**Returns:**

- `Optional[pathspec.PathSpec]`: A PathSpec object containing the patterns from .gitignore if respect_gitignore
    is True and the .gitignore file exists, None otherwise.
