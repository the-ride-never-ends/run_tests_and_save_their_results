import unittest
from unittest.mock import MagicMock, patch

from reports.services.flake8 import Flake8Collector

class TestFlake8Collector(unittest.TestCase):
    """
    Test case for the Flake8Collector class.
    """

    def setUp(self):
        """
        Setup test fixtures for each test.
        """
        self.mock_configs = MagicMock()
        self.mock_resources = {'runner': MagicMock()}
        self.collector = Flake8Collector(configs=self.mock_configs, resources=self.mock_resources)

    def test_initialization(self):
        """
        Test that the collector is initialized correctly.
        """
        self.assertEqual(self.collector.name, "flake8")
        self.assertEqual(self.collector.configs, self.mock_configs)
        self.assertEqual(self.collector.resources, self.mock_resources)

    def test_initialization_with_none_values(self):
        """
        Test that the collector handles None values for configs and resources.
        """
        collector = Flake8Collector(configs=None, resources=None)
        self.assertEqual(collector.name, "flake8")
        self.assertIsNone(collector.configs)
        self.assertIsNone(collector.resources)

    def test_initialization_with_custom_values(self):
        """
        Test that the collector handles custom configs and resources.
        """
        custom_configs = {'option': 'value'}
        custom_resources = {'tool': 'flake8'}
        collector = Flake8Collector(configs=custom_configs, resources=custom_resources)
        self.assertEqual(collector.name, "flake8")
        self.assertEqual(collector.configs, custom_configs)
        self.assertEqual(collector.resources, custom_resources)

    @patch('reports.collector.Collector.__init__')
    def test_parent_constructor_called(self, mock_init):
        """
        Test that the parent constructor is called with the right parameters.
        """
        mock_init.return_value = None
        configs = {'setting': 'value'}
        resources = {'dependency': 'injected'}
        collector = Flake8Collector(configs=configs, resources=resources)
        
        mock_init.assert_called_once_with(configs, resources, name="flake8")


if __name__ == "__main__":
    unittest.main()