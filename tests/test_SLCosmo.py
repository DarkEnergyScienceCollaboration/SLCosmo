"""
Unit tests for SLCosmo class
"""
import os
import numpy as np
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
        self.Lets.make_some_mock_data(13)
        self.assertEquals(len(self.Lets.lenses), 13)
        for k in range(len(self.Lets.lenses)):
            self.assertEqual(len(self.Lets.lenses[k].DeltaFP_obs),
                             self.Lets.lenses[k].Nim - 1)

    def test_factory_and_read_in_time_delay_samples(self):
        self.Lets.make_some_mock_data(21, quad_fraction=0.2,
                                      stem="test_SLCosmo")
        We = desc.slcosmo.SLCosmo()
        We.read_in_time_delay_samples_from(self.Lets.mock_files)

        self.assertEqual(len(self.Lets.lenses), len(We.lenses))
        for k in range(len(We.lenses)):
            # print "Testing ",self.Lets.mock_files[k]
            self.assertEqual(self.Lets.mock_files[k],
                             We.lenses[k].source)
            self.assertEqual(self.Lets.lenses[k].Nim,
                             We.lenses[k].Nim)


if __name__ == '__main__':
    unittest.main()
