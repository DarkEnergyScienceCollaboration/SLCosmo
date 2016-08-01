"""
Unit tests for SLCosmo class
"""
import os
import unittest
import desc.slcosmo

class SLCosmoUnitTestCase(unittest.TestCase):

    def setUp(self):
        "Create an SLCosmo object to be used in each of the tests."
        self.Lets = desc.slcosmo.SLCosmo()

    def tearDown(self):
        "Clean up any mock data files created by the tests."
        for mock_file in self.Lets.mock_files:
            os.remove(mock_file)

    def test_factory(self):
        self.Lets.make_some_mock_data(3)
        self.assertEquals(len(self.Lets.lenses), 3)

    def test_read_in_time_delay_samples(self):
        self.Lets.make_some_mock_data(1)
        self.Lets.read_in_time_delay_samples(self.Lets.mock_files)
        self.assertEqual(len(self.Lets.lenses), 1)
        self.assertEqual(self.Lets.Nlenses, 1)

if __name__ == '__main__':
    unittest.main()
