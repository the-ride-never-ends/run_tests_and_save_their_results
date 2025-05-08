"""
Generate reports for code style linting with flake8.
Uses inversion of control with dependency injection for better testability.
"""
from typing import Any, Dict, List

from reports.collector import Collector


class Flake8Collector(Collector):
    """
    Collects and formats code style results for reporting.
    Uses inversion of control pattern.
    """

    def __init__(self, configs=None, resources=None):
        """
        Initialize the collector with configs and resources.
        
        Args:
            configs: Configuration dataclass
            resources: Dictionary of resources used by the collector
        """
        # Initialize with base constructor, passing the name
        super().__init__(configs, resources, name="flake8")