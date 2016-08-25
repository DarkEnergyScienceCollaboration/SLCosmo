"""
Scientific tests for SLCosmo package
"""
import matplotlib
matplotlib.use('Agg')
import os
import unittest
import desc.slcosmo

class SLCosmoScienceTestCase(unittest.TestCase):

    def setUp(self):
        self.message = 'Testing SLCosmo - For Science!'
        self.Lets = desc.slcosmo.SLCosmo()

    def tearDown(self):
        "Clean up any mock data files created by the tests."
        for mock_file in self.Lets.mock_files:
            os.remove(mock_file)

    def test_round_trip(self):
        self.Lets.make_some_mock_data(Nlenses=10, Nsamples=20)
        self.Lets.draw_some_prior_samples(Npriorsamples=100)
        self.Lets.compute_the_joint_log_likelihood()
        self.Lets.report_the_inferred_cosmological_parameters()
        self.Lets.plot_the_inferred_cosmological_parameters()
        H0, sigma = self.Lets.estimate_H0()
        lower_limit = H0 - 3.0*sigma
        upper_limit = H0 + 3.0*sigma
        self.assertGreater(self.Lets.cosmotruth['H0'], lower_limit)
        self.assertLess(self.Lets.cosmotruth['H0'], upper_limit)



if __name__ == '__main__':
    unittest.main()
