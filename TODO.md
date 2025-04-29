# TODO for run_tests_and_save_their_results

A prioritized list of tasks for improving the test runner and report generator.

### Todo

- [ ] Fix CornerCuttingCollector implementation
  - [ ] Fix undefined variables in run() method
  - [ ] Fix report variable reference in generate_markdown_report()
  - [ ] Add proper error handling

- [ ] Implement code coverage reporting
  - [ ] Add coverage.py integration
  - [ ] Include coverage percentage in test reports
  - [ ] Generate HTML coverage reports

- [ ] Add support for additional testing frameworks
  - [ ] Add pytest support
  - [ ] Make test runner framework-agnostic

- [ ] Improve report formatting
  - [ ] Add color-coding to markdown reports
  - [ ] Include test runtime performance metrics
  - [ ] Add trend indicators compared to previous runs

- [ ] Refactor collector classes to enhance inversion of control.
  - [ ] Implement an interface class with control logic
  - [ ] Use dependency injection for collector classes

- [ ] Add custom ignore patterns support
  - [ ] Implement .testignore file specification
  - [ ] Support glob pattern matching for ignored files

- [ ] Enhance documentation
  - [ ] Add usage examples for each collector
  - [ ] Add type hints to all functions
  - [ ] Include more complex usage examples

### In Progress

- [ ] Fix handling of test_dir parameter [CLI-123]
  - [ ] Add validation for directory existence
  - [ ] Improve error messages

### Done ✓

- [x] Implement basic test report generation 2025-04-15
- [x] Add linting report with flake8 integration 2025-04-18
- [x] Add type checking report with mypy integration 2025-04-20