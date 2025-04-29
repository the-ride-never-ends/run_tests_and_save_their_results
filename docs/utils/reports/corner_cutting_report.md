# corner_cutting_report.py: last updated 03:33 PM on April 27, 2025

**File Path:** `run_tests_and_save_their_results/utils/reports/corner_cutting_report.py`

## Module Description

Script to identify corner cutting in a given file.
Corner cutting is defined as implementation shortcuts, temporary solutions, or placeholders 
that are likely to need improvement or replacement in the future.

Corner cutting is identified programmatically by checking for the presence of certain keywords in the file's comments and docstrings.

## Table of Contents

### Classes

- [`CornerCuttingCollector`](#cornercuttingcollector)

## Classes

## `CornerCuttingCollector`

```python
class CornerCuttingCollector(object)
```

**Methods:**

- [`_extract_docstrings_ast`](#_extract_docstrings_ast) (static method)
- [`_extract_docstrings_regex`](#_extract_docstrings_regex) (static method)
- [`_extract_single_line_comments`](#_extract_single_line_comments) (static method)
- [`generate_markdown_report`](#generate_markdown_report)
- [`identify_corner_cutting`](#identify_corner_cutting)
- [`load_lazy_words`](#load_lazy_words) (static method)
- [`run`](#run)

### `_extract_docstrings_ast`

```python
@staticmethod
def _extract_docstrings_ast(file_content, comments_and_docstrings)
```

Extract docstrings from Python code using the AST module.

Recursively finds all docstrings in modules, classes, and functions
in the provided code and adds them to the comments_and_docstrings list.

**Parameters:**

- `file_content` (`str`): String containing Python source code to analyze.

- `comments_and_docstrings` (`list`): list to which extracted docstrings will be added
  as (docstring_line, line_number) tuples.

**Raises:**

- `SyntaxError`: If the Python code cannot be parsed by the AST module.

### `_extract_docstrings_regex`

```python
@staticmethod
def _extract_docstrings_regex(file_content, comments_and_docstrings)
```

Extract docstrings using regex to find them.

**Parameters:**

- `file_content (str)` (`Any`): The content of the Python file.

- `comments_and_docstrings (list)` (`Any`): list to store extracted comments and docstrings.

### `_extract_single_line_comments`

```python
@staticmethod
def _extract_single_line_comments(file_content, comments_and_docstrings)
```

Extracts single-line comments from Python code.
This static method parses a file's content line by line to identify single-line
comments (starting with '#') while properly handling cases where '#' characters
appear inside string literals.

**Parameters:**

- `file_content (str)` (`Any`): The content of the Python file as a string.

- `comments_and_docstrings (list)` (`Any`): A list to which extracted comments will be added.
  Each comment is added as a tuple of (comment_text, line_number).

**Returns:**

- `list[tuple[(str, int)]]`: A list of tuples containing the comment text and corresponding
        line number, though the function actually modifies the input list in-place.

### `generate_markdown_report`

```python
def generate_markdown_report(self)
```

Generate a Markdown report of the corner cutting instances.

**Parameters:**

- `report (dict)` (`Any`): The corner cutting report.

**Returns:**

- `str`: The Markdown report as a string.

### `identify_corner_cutting`

```python
def identify_corner_cutting(self, file_path)
```

Identify instances of corner cutting in a file by checking for 
lazy words and phrases in comments and docstrings.

**Parameters:**

- `file_path (str)` (`Any`): The path to the file to check.

**Returns:**

- `dict[(str, list[tuple[(str, int)]])]`: A dictionary mapping lazy words
    to lists of tuples containing the context and line number.

### `load_lazy_words`

```python
@staticmethod
def load_lazy_words()
```

Load the list of lazy words and phrases from the JSON file.

**Returns:**

- `list[str]`: A list of words and phrases that indicate corner cutting.

### `run`

```python
def run(self, target_dir)
```

Generate a report of corner cutting instances in a file.

**Parameters:**

- `file_path (str)` (`Any`): The path to the file to check.

**Returns:**

- `dict`: A report containing information about corner cutting instances.
