# TODO for run_tests_and_save_their_results

A prioritized list of tasks for improving the test runner and report generator.

### Todo

- [ ] Debugging
  - [ ] Fix path ignore so that flake and mypy skip virtual environment, dependencies, and deprecated files/folders.
  - [ ] Write dedicated tests for corner cutting collector to verify its functionality.

- [ ] Refactoring.
  - [ ] Factor out poltergeist classes in reports/services.
  - [ ] Prune unused code and files.
  - [ ] Linting.
    - [ ] Remove unused imports and variables
    - [ ] Fix PEP8 violations
    - [ ] Add type hints to all functions and methods
    - [ ] Ensure all functions and methods have docstrings

- [ ] Add more configuration options
  - [ ] Ability to load CLI arguments from a JSON config file.
  - [ ] Add ignore checks for mypy and flake8.
    - [ ] Ignore  

- [ ] Fix remaining issues in CornerCuttingCollector implementation
  - [ ] Fix undefined variables in run() method
  - [ ] Fix report variable reference in generate_markdown_report()
  - [ ] Add proper error handling

- [ ] Implement code coverage reporting
  - [ ] Add coverage.py integration
  - [ ] Include coverage percentage in test reports
  - [ ] Generate HTML coverage reports
  - [ ] Add coverage badge generation for README.md

- [ ] Add support for additional testing frameworks
  - [ ] Add pytest support
  - [ ] Make test runner framework-agnostic
  - [ ] Support async test frameworks

- [ ] Improve report formatting
  - [ ] Add color-coding to markdown reports
  - [ ] Include test runtime performance metrics
  - [ ] Add trend indicators compared to previous runs
  - [ ] Generate summary graphs for long-term tracking

- [ ] Add custom ignore patterns support
  - [ ] Implement .testignore file specification
  - [ ] Support glob pattern matching for ignored files
  - [ ] Add command-line flag to specify custom ignore patterns

- [ ] Enhance README
  - [ ] Add usage examples for each collector
  - [ ] Include more complex usage examples
  - [ ] Create detailed architectural documentation

- [ ] Improve the CLI and error handling
  - [ ] Add better error messages for common issues
  - [ ] Implement debug mode for troubleshooting
  - [ ] Add progress bars for long-running operations

### In Progress

- [ ] Fix handling of test_dir parameter [CLI-123]
  - [ ] Add validation for directory existence
  - [ ] Improve error messages

### Done ✓

5-8-2025
- [x] Implement inversion of control for collector classes
  - [x] Design new collector structure using dependency injection
  - [x] Create tests for the base collector with IoC pattern
  - [x] Implement the base collector structure according to tests
  - [x] Refactor UnittestCollector to use dependency injection
    - [x] Extract run_command functionality to a separate module
    - [x] Extract parse_output functionality to a separate module
    - [x] Extract format_report functionality to a separate module
    - [x] Implement the refactored UnittestCollector
  - [x] Refactor Flake8Collector to use dependency injection
    - [x] Extract run_command functionality to a separate module
    - [x] Extract parse_output functionality to a separate module
    - [x] Extract format_report functionality to a separate module
    - [x] Implement the refactored Flake8Collector
  - [x] Refactor MyPyCollector to use dependency injection
    - [x] Extract run_command functionality to a separate module
    - [x] Extract parse_output functionality to a separate module
    - [x] Extract format_report functionality to a separate module
    - [x] Implement the refactored MyPyCollector
  - [x] Refactor CornerCuttingCollector to use dependency injection
    - [x] Extract run_command functionality to a separate module
    - [x] Extract parse_output functionality to a separate module
    - [x] Extract format_report functionality to a separate module
    - [x] Implement the refactored CornerCuttingCollector
  - [x] Write tests for specific collector implementations
  - [x] Update main.py to use the new collector implementations
  - [x] Add necessary functions to resources dictionary
  - [x] Run the tests to verify the implementation
  - [x] Update documentation to reflect the new IoC pattern
  - [x] Fix collector name initialization to properly pass name to create_results function
  - [x] Release version 0.2.0 with completed IoC implementation

- [x] Implement basic test report generation 2025-04-15
- [x] Add linting report with flake8 integration 2025-04-18
- [x] Add type checking report with mypy integration 2025-04-20