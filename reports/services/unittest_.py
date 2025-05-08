"""
Run unittest tests for Test Generator tool, then save the results to json and markdown.
Uses inversion of control with dependency injection for better testability.
"""
from typing import Any, Dict, Callable, Optional, List

from reports.collector import Collector


class UnittestCollector(Collector):
    """
    Discovers and runs unit tests, then generates reports using dependency injection.
    """

    def __init__(self, configs=None, resources=None):
        """
        Initialize the collector with configs and resources.
        
        Args:
            configs: Configuration dataclass
            resources: Dictionary of resources used by the collector
        """
        # Initialize with base constructor, passing the name
        super().__init__(configs, resources, name="unittest")