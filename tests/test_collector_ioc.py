#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the collector classes using inversion of control.
"""
import unittest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import Dict, Any, Callable, List


@dataclass
class TestConfigs:
    """Test configuration class."""
    test_dir: str = "test_dir"
    reports_dir: str = "reports_dir"
    respect_gitignore: bool = False
    verbosity: int = 2
    gitignore_spec = None


class TestResults:
    """Test results class."""
    
    def __init__(self, name):
        self.name = name
        self.errors = 0
        self.tests = 0
        self.failures = 0
        self.status = "not_run"
        self.issues = []
        self.test_cases = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to a dictionary."""
        return {
            "summary": {
                "name": self.name,
                "errors": self.errors,
                "status": self.status
            }
        }


class TestCollector:
    """Test collector class with IoC pattern."""
    
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
        self.name = "test"
        self.results = self.resources.get("create_results", lambda x: None)(self.name)
        
        # Extract resource functions
        self._run_command = self.resources.get("run_command")
        self._parse_output = self.resources.get("parse_output")
        self._format_report = self.resources.get("format_report")

    def run(self):
        """
        Run the test command and collect results.
        
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


class TestCollectorIOC(unittest.TestCase):
    """Test the collector IoC pattern."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.configs = TestConfigs()
        
        # Create mock functions
        self.mock_run_command = MagicMock(return_value="test output")
        self.mock_parse_output = MagicMock(return_value=True)
        self.mock_format_report = MagicMock(return_value=["# Test Report", "Line 1", "Line 2"])
        self.mock_create_results = MagicMock(return_value=TestResults("test"))
        
        # Create resources dictionary
        self.resources = {
            "create_results": self.mock_create_results,
            "run_command": self.mock_run_command,
            "parse_output": self.mock_parse_output,
            "format_report": self.mock_format_report
        }
        
        # Create collector
        self.collector = TestCollector(configs=self.configs, resources=self.resources)
    
    def test_initialization(self):
        """Test that the collector initializes correctly."""
        # Verify that the collector has the correct attributes
        self.assertEqual(self.collector.name, "test")
        self.assertEqual(self.collector.configs, self.configs)
        self.assertEqual(self.collector.resources, self.resources)
        
        # Verify that create_results was called with the correct name
        self.mock_create_results.assert_called_once_with("test")
        
        # Verify that the collector has the correct resource methods
        self.assertEqual(self.collector._run_command, self.mock_run_command)
        self.assertEqual(self.collector._parse_output, self.mock_parse_output)
        self.assertEqual(self.collector._format_report, self.mock_format_report)
    
    def test_run_method(self):
        """Test that the run method works correctly."""
        # Call the run method
        result = self.collector.run()
        
        # Verify that run_command was called with the correct configs
        self.mock_run_command.assert_called_once_with(self.configs)
        
        # Verify that parse_output was called with the correct arguments
        self.mock_parse_output.assert_called_once_with("test output", self.collector.results)
        
        # Verify that the result is what we expect
        self.assertTrue(result)
    
    def test_generate_markdown_report(self):
        """Test that the generate_markdown_report method works correctly."""
        # Call the generate_markdown_report method
        result = self.collector.generate_markdown_report()
        
        # Verify that format_report was called with the correct results
        self.mock_format_report.assert_called_once_with(self.collector.results)
        
        # Verify that the result is what we expect
        self.assertEqual(result, ["# Test Report", "Line 1", "Line 2"])
    
    def test_missing_resources(self):
        """Test that the collector handles missing resources gracefully."""
        # Create collector with empty resources
        collector = TestCollector(configs=self.configs, resources={})
        
        # Verify that the collector has None for resource methods
        self.assertIsNone(collector._run_command)
        self.assertIsNone(collector._parse_output)
        self.assertIsNone(collector._format_report)
        
        # Verify that results is None (since create_results is missing)
        self.assertIsNone(collector.results)
    
    def test_with_real_resource_functions(self):
        """Test the collector with actual functions instead of mocks."""
        # Create real functions
        def create_results(name):
            return TestResults(name)
            
        def run_command(configs):
            return "Real test output"
            
        def parse_output(output, results):
            results.errors = 0
            results.status = "pass"
            return True
            
        def format_report(results):
            return [
                "# Real Test Report",
                f"Status: {results.status}",
                f"Errors: {results.errors}"
            ]
        
        # Create resources dictionary with real functions
        resources = {
            "create_results": create_results,
            "run_command": run_command,
            "parse_output": parse_output,
            "format_report": format_report
        }
        
        # Create collector with real functions
        collector = TestCollector(configs=self.configs, resources=resources)
        
        # Run the collector
        result = collector.run()
        
        # Verify that the run was successful
        self.assertTrue(result)
        
        # Verify that the results were updated
        self.assertEqual(collector.results.status, "pass")
        self.assertEqual(collector.results.errors, 0)
        
        # Generate report
        report = collector.generate_markdown_report()
        
        # Verify the report
        self.assertEqual(report, [
            "# Real Test Report",
            "Status: pass",
            "Errors: 0"
        ])


# Additional test for a specific collector implementation
class TestUnittestCollectorIOC(unittest.TestCase):
    """Test the UnittestCollector with IoC."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.configs = TestConfigs()
        
        # Create mock test result
        self.mock_output = "Ran 10 tests in 0.123s\n\nOK"
        
        # Create mock functions for Unittest collector
        self.mock_run_unittest = MagicMock(return_value=self.mock_output)
        self.mock_process_results = MagicMock(return_value=True)
        self.mock_format_unittest_report = MagicMock(return_value=["# Unittest Report"])
        self.mock_create_results = MagicMock(return_value=TestResults("unittest"))
        
        # Create resources dictionary
        self.resources = {
            "create_results": self.mock_create_results,
            "run_command": self.mock_run_unittest,
            "parse_output": self.mock_process_results,
            "format_report": self.mock_format_unittest_report
        }
        
        # Import the actual UnittestCollector
        from reports.collector import Collector
        from reports.services.unittest_ import UnittestCollector
        self.collector_class = UnittestCollector
        
        # Create collector instance
        self.collector = self.collector_class(configs=self.configs, resources=self.resources)
        
    def test_unittest_collector_initialization(self):
        """Test that the UnittestCollector initializes correctly."""
        # Verify the collector name is set correctly
        self.assertEqual(self.collector.name, "unittest")
        
        # Verify that create_results was called with the correct name
        self.mock_create_results.assert_called_once_with("unittest")
        
        # Check that resources were properly assigned
        self.assertEqual(self.collector._run_command, self.mock_run_unittest)
        self.assertEqual(self.collector._parse_output, self.mock_process_results)
        self.assertEqual(self.collector._format_report, self.mock_format_unittest_report)
    
    def test_unittest_collector_run_method(self):
        """Test that the UnittestCollector.run method works correctly."""
        # Call the run method
        result = self.collector.run()
        
        # Verify that run_command was called with the correct configs
        self.mock_run_unittest.assert_called_once_with(self.configs)
        
        # Verify that parse_output was called with the correct arguments
        self.mock_process_results.assert_called_once_with(self.mock_output, self.collector.results)
        
        # Verify that the result is what we expect
        self.assertTrue(result)
    
    def test_unittest_collector_generate_markdown_report(self):
        """Test that the UnittestCollector.generate_markdown_report method works correctly."""
        # Call the generate_markdown_report method
        result = self.collector.generate_markdown_report()
        
        # Verify that format_report was called with the correct results
        self.mock_format_unittest_report.assert_called_once_with(self.collector.results)
        
        # Verify that the result is what we expect
        self.assertEqual(result, ["# Unittest Report"])


# Additional test for the Flake8Collector implementation
class TestFlake8CollectorIOC(unittest.TestCase):
    """Test the Flake8Collector with IoC."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.configs = TestConfigs()
        
        # Create mock flake8 output
        self.mock_output = "./file.py:10:5: E303 too many blank lines (3)"
        
        # Create mock functions for Flake8 collector
        self.mock_run_flake8 = MagicMock(return_value=self.mock_output)
        self.mock_process_flake8_output = MagicMock(return_value=True)
        self.mock_format_flake8_report = MagicMock(return_value=["# Flake8 Report"])
        self.mock_create_results = MagicMock(return_value=TestResults("flake8"))
        
        # Create resources dictionary
        self.resources = {
            "create_results": self.mock_create_results,
            "run_command": self.mock_run_flake8,
            "parse_output": self.mock_process_flake8_output,
            "format_report": self.mock_format_flake8_report
        }
        
        # Import the actual Flake8Collector
        from reports.collector import Collector
        from reports.services.flake8 import Flake8Collector
        self.collector_class = Flake8Collector
        
        # Create collector instance
        self.collector = self.collector_class(configs=self.configs, resources=self.resources)
    
    def test_flake8_collector_initialization(self):
        """Test that the Flake8Collector initializes correctly."""
        # Verify the collector name is set correctly
        self.assertEqual(self.collector.name, "flake8")
        
        # Verify that create_results was called with the correct name
        self.mock_create_results.assert_called_once_with("flake8")
        
        # Check that resources were properly assigned
        self.assertEqual(self.collector._run_command, self.mock_run_flake8)
        self.assertEqual(self.collector._parse_output, self.mock_process_flake8_output)
        self.assertEqual(self.collector._format_report, self.mock_format_flake8_report)
    
    def test_flake8_collector_run_method(self):
        """Test that the Flake8Collector.run method works correctly."""
        # Call the run method
        result = self.collector.run()
        
        # Verify that run_command was called with the correct configs
        self.mock_run_flake8.assert_called_once_with(self.configs)
        
        # Verify that parse_output was called with the correct arguments
        self.mock_process_flake8_output.assert_called_once_with(self.mock_output, self.collector.results)
        
        # Verify that the result is what we expect
        self.assertTrue(result)
    
    def test_flake8_collector_generate_markdown_report(self):
        """Test that the Flake8Collector.generate_markdown_report method works correctly."""
        # Call the generate_markdown_report method
        result = self.collector.generate_markdown_report()
        
        # Verify that format_report was called with the correct results
        self.mock_format_flake8_report.assert_called_once_with(self.collector.results)
        
        # Verify that the result is what we expect
        self.assertEqual(result, ["# Flake8 Report"])


# Additional test for the MyPyCollector implementation
class TestMyPyCollectorIOC(unittest.TestCase):
    """Test the MyPyCollector with IoC."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.configs = TestConfigs()
        
        # Create mock mypy output
        self.mock_output = "file.py:15: error: Incompatible types in assignment (expression has type \"int\", variable has type \"str\") [assignment]"
        
        # Create mock functions for MyPy collector
        self.mock_run_mypy = MagicMock(return_value=self.mock_output)
        self.mock_process_mypy_output = MagicMock(return_value=True)
        self.mock_format_mypy_report = MagicMock(return_value=["# MyPy Report"])
        self.mock_create_results = MagicMock(return_value=TestResults("mypy"))
        
        # Create resources dictionary
        self.resources = {
            "create_results": self.mock_create_results,
            "run_command": self.mock_run_mypy,
            "parse_output": self.mock_process_mypy_output,
            "format_report": self.mock_format_mypy_report
        }
        
        # Import the actual MyPyCollector
        from reports.collector import Collector
        from reports.services.mypy import MyPyCollector
        self.collector_class = MyPyCollector
        
        # Create collector instance
        self.collector = self.collector_class(configs=self.configs, resources=self.resources)
    
    def test_mypy_collector_initialization(self):
        """Test that the MyPyCollector initializes correctly."""
        # Verify the collector name is set correctly
        self.assertEqual(self.collector.name, "mypy")
        
        # Verify that create_results was called with the correct name
        self.mock_create_results.assert_called_once_with("mypy")
        
        # Check that resources were properly assigned
        self.assertEqual(self.collector._run_command, self.mock_run_mypy)
        self.assertEqual(self.collector._parse_output, self.mock_process_mypy_output)
        self.assertEqual(self.collector._format_report, self.mock_format_mypy_report)
    
    def test_mypy_collector_run_method(self):
        """Test that the MyPyCollector.run method works correctly."""
        # Call the run method
        result = self.collector.run()
        
        # Verify that run_command was called with the correct configs
        self.mock_run_mypy.assert_called_once_with(self.configs)
        
        # Verify that parse_output was called with the correct arguments
        self.mock_process_mypy_output.assert_called_once_with(self.mock_output, self.collector.results)
        
        # Verify that the result is what we expect
        self.assertTrue(result)
    
    def test_mypy_collector_generate_markdown_report(self):
        """Test that the MyPyCollector.generate_markdown_report method works correctly."""
        # Call the generate_markdown_report method
        result = self.collector.generate_markdown_report()
        
        # Verify that format_report was called with the correct results
        self.mock_format_mypy_report.assert_called_once_with(self.collector.results)
        
        # Verify that the result is what we expect
        self.assertEqual(result, ["# MyPy Report"])


# Additional test for the CornerCuttingCollector implementation
class TestCornerCuttingCollectorIOC(unittest.TestCase):
    """Test the CornerCuttingCollector with IoC."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.configs = TestConfigs()
        
        # Create mock corner cutting scan results
        self.mock_output = {
            "total_files_scanned": 10,
            "issues": [
                {
                    "file": "file.py",
                    "line": 15,
                    "category": "TODO",
                    "pattern": "TODO",
                    "message": "Found TODO comment",
                    "snippet": "# TODO: Fix this later"
                }
            ]
        }
        
        # Create mock functions for CornerCutting collector
        self.mock_run_corner_cutting = MagicMock(return_value=self.mock_output)
        self.mock_process_corner_cutting_output = MagicMock(return_value=False)  # False because issues were found
        self.mock_format_corner_cutting_report = MagicMock(return_value=["# Corner Cutting Report"])
        self.mock_create_results = MagicMock(return_value=TestResults("corner_cutting"))
        
        # Create resources dictionary
        self.resources = {
            "create_results": self.mock_create_results,
            "run_command": self.mock_run_corner_cutting,
            "parse_output": self.mock_process_corner_cutting_output,
            "format_report": self.mock_format_corner_cutting_report
        }
        
        # Import the actual CornerCuttingCollector
        from reports.collector import Collector
        from reports.services.corner_cutting import CornerCuttingCollector
        self.collector_class = CornerCuttingCollector
        
        # Create collector instance
        self.collector = self.collector_class(configs=self.configs, resources=self.resources)
    
    def test_corner_cutting_collector_initialization(self):
        """Test that the CornerCuttingCollector initializes correctly."""
        # Verify the collector name is set correctly
        self.assertEqual(self.collector.name, "corner_cutting")
        
        # Verify that create_results was called with the correct name
        self.mock_create_results.assert_called_once_with("corner_cutting")
        
        # Check that resources were properly assigned
        self.assertEqual(self.collector._run_command, self.mock_run_corner_cutting)
        self.assertEqual(self.collector._parse_output, self.mock_process_corner_cutting_output)
        self.assertEqual(self.collector._format_report, self.mock_format_corner_cutting_report)
    
    def test_corner_cutting_collector_run_method(self):
        """Test that the CornerCuttingCollector.run method works correctly."""
        # Call the run method
        result = self.collector.run()
        
        # Verify that run_command was called with the correct configs
        self.mock_run_corner_cutting.assert_called_once_with(self.configs)
        
        # Verify that parse_output was called with the correct arguments
        self.mock_process_corner_cutting_output.assert_called_once_with(self.mock_output, self.collector.results)
        
        # Verify that the result is what we expect (should be False since we mocked issues)
        self.assertFalse(result)
    
    def test_corner_cutting_collector_generate_markdown_report(self):
        """Test that the CornerCuttingCollector.generate_markdown_report method works correctly."""
        # Call the generate_markdown_report method
        result = self.collector.generate_markdown_report()
        
        # Verify that format_report was called with the correct results
        self.mock_format_corner_cutting_report.assert_called_once_with(self.collector.results)
        
        # Verify that the result is what we expect
        self.assertEqual(result, ["# Corner Cutting Report"])


if __name__ == "__main__":
    unittest.main()