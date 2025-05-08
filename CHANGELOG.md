# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Created design document for refactoring collectors to use inversion of control
- Added tests for testing the collector IoC pattern
- Created base collector class implementing the inversion of control pattern
- Added utility functions for each collector's responsibilities (run_command, parse_output, format_report)
- Added tests for each collector implementation (UnittestCollector, Flake8Collector, MyPyCollector, CornerCuttingCollector)

### Changed

- Refactored all collector classes to use dependency injection instead of inheritance
- Moved original collector implementations to deprecated/ directory
- Separated the responsibility of each collector into discrete utility functions

## [0.1.0] - 2025-04-20

### Added

- Initial implementation of test runners and report generators
- Added unittest test runner
- Added flake8 linting runner
- Added mypy type checking runner
- Added basic report generation in JSON and Markdown formats

[unreleased]: https://github.com/username/repository/compare/vx.y.z...HEAD
[x.y.z]: https://github.com/username/repository/compare/va.b.c...vx.y.z
[a.b.c]: https://github.com/username/repository/releases/tag/va.b.c