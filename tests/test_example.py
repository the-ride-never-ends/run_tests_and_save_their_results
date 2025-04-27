#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example test module to demonstrate the test runner.
"""
import unittest


class ExampleTest(unittest.TestCase):
    """Example test case."""

    def test_addition(self):
        """Test that addition works."""
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        """Test that subtraction works."""
        self.assertEqual(3 - 1, 2)
    
    def test_multiplication(self):
        """Test that multiplication works."""
        self.assertEqual(2 * 2, 4)
    
    @unittest.skip("Example of a skipped test")
    def test_skipped(self):
        """This test is skipped as an example."""
        self.fail("This should be skipped")


if __name__ == "__main__":
    unittest.main()