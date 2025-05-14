#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base collector interface for running tests and generating reports.
Using inversion of control pattern for configuration and resource management.
"""
from typing import Any, Dict, List, Callable, Optional


class Collector:
    """
    Base collector class for test runners and report generators.
    Implements the inversion of control pattern for better testability and flexibility.
    """

    def __init__(self, configs=None, resources=None, name="base"):
        """
        Initialize the collector with configs and resources.
        
        Args:
            configs: Configuration dataclass
            resources: Dictionary of resources used by the collector
            name: Name of the collector
        """
        self.configs = configs or {}
        self.resources = resources or {}
        
        # Set collector name
        self.name = self.resources.get("name", "base")
        
        # Create results with collector name
        self._create_results = self.resources["create_results"]
        self.results = self._create_results(self.name)
        
        # Extract resource functions
        self._run_command = self.resources["run_command"]
        self._parse_output = self.resources["parse_output"]
        self._format_report = self.resources["format_report"]

    def run(self) -> bool:
        """
        Run the test/linting command and collect results.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._run_command or not self._parse_output:
            raise ValueError("Required resources missing: run_command and/or parse_output")
            
        # Use resources to run command
        output = self._run_command(self.configs)
        
        # Use resources to parse output
        success: bool = self._parse_output(output, self.results)
        
        self.results.status = "pass" if success else "fail"
        
        return success

    def generate_markdown_report(self) -> List[str]:
        """
        Generate a Markdown report of the results.
        
        Returns:
            List[str]: Lines of the markdown report
        """
        if not self._format_report:
            raise ValueError("Required resource missing: format_report")
            
        # Use resources to format the report
        return self._format_report(self.results)