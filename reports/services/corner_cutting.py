"""
Generate reports for corner-cutting detection in the codebase.
Uses inversion of control with dependency injection for better testability.
"""
from typing import Any, Dict, List

from reports.collector import Collector


class CornerCuttingCollector(Collector):
    """
    Scans codebase for potential corner-cutting indicators.
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
        super().__init__(configs, resources, name="corner_cutting")