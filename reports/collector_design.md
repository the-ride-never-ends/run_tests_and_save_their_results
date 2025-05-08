# Collector Design

## Overview

This document outlines the design for implementing inversion of control (IoC) using dependency injection for the test collectors in the run_tests_and_save_their_results tool.

## Current Issues

The current implementation has several issues:

1. Collectors mix orchestration logic with implementation details
2. Dependencies are hardcoded inside collector classes
3. Configurations are passed inconsistently
4. Testing is difficult because dependencies are tightly coupled

## New Design

### Key Principles

1. Use dependency injection through the constructor
2. Separate orchestration logic from implementation details
3. Pass dependencies through a resources dictionary
4. Pass configurations through a dedicated configs parameter

### Collector Interface

All collectors will follow this interface pattern:

```python
class ExampleCollector:
    """Collects and processes test results."""

    def __init__(self, configs=None, resources=None):
        """
        Initialize the collector with configs and resources.
        
        Args:
            configs: Configuration dataclass
            resources: Dictionary of resources used by the collector
        """
        self.configs = configs or {}
        self.resources = resources or {}
        
        # Extract configuration values
        self.name = "example"
        self.results = self.resources.get("create_results", lambda x: None)(self.name)
        
        # Extract resource functions
        self._run_command = self.resources.get("run_command")
        self._parse_output = self.resources.get("parse_output")
        self._format_report = self.resources.get("format_report")

    def run(self):
        """
        Run the test/linting command and collect results.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Use resources to run command
        output = self._run_command(self.configs)
        
        # Use resources to parse output
        success = self._parse_output(output, self.results)
        
        return success

    def generate_markdown_report(self):
        """
        Generate a Markdown report of the results.
        
        Returns:
            List[str]: Lines of the markdown report
        """
        # Use resources to format the report
        return self._format_report(self.results)
```

### Resources Organization

Resources will be split into separate utility modules:

```
reports/
├── __init__.py
├── collector.py  # Define empty interface file
├── services/
│   ├── __init__.py
│   ├── unittest_.py  # Collector implementation
│   ├── flake8.py     # Collector implementation
│   ├── mypy.py       # Collector implementation
│   └── corner_cutting.py  # Collector implementation
└── utils/
    ├── __init__.py
    ├── unittest/
    │   ├── __init__.py
    │   ├── run_command.py
    │   ├── parse_output.py
    │   └── format_report.py
    ├── flake8/
    │   ├── __init__.py
    │   ├── run_command.py
    │   ├── parse_output.py
    │   └── format_report.py
    └── ...
```

### Refactored Main Entry Point

The main entry point will create resources and configs, then pass them to collectors:

```python
def main():
    # Parse arguments and create configs
    configs = Configs(...)
    
    # Create resource dictionaries for each collector
    unittest_resources = {
        "create_results": lambda name: Results(name=name),
        "run_command": run_unittest_command,
        "parse_output": parse_unittest_output,
        "format_report": format_unittest_report
    }
    
    flake8_resources = {
        "create_results": lambda name: Results(name=name),
        "run_command": run_flake8_command,
        "parse_output": parse_flake8_output,
        "format_report": format_flake8_report
    }
    
    # Create collectors with their resources
    collectors = []
    if run_tests:
        collectors.append(UnittestCollector(configs=configs, resources=unittest_resources))
    if run_flake8:
        collectors.append(Flake8Collector(configs=configs, resources=flake8_resources))
    # ...
    
    # Create the test runner with these collectors
    resources = {"collectors": collectors}
    runner = RunTestsAndSaveTheirResults(configs=configs, resources=resources)
    runner.run()
```

### Benefits

1. Better testability - can mock all dependencies
2. Clearer separation of concerns
3. More maintainable code structure
4. Follows the project architectural guidelines
5. Dependencies can be easily swapped or modified
6. Configuration changes don't require modifying the collector classes

## Implementation Plan

1. Create utility functions for each collector
2. Refactor each collector to use dependency injection
3. Update the main script to provide resources
4. Test the new implementation thoroughly