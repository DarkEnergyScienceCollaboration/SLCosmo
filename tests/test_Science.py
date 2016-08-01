"""
Scientific tests for SLCosmo package
"""
import matplotlib
matplotlib.use('Agg')
import unittest
import desc.slcosmo

class SLCosmoScienceTestCase(unittest.TestCase):

    def setUp(self):
        self.message = 'Testing SLCosmo - For Science!'

    def tearDown(self):
        pass

    def test_round_trip(self):
        Lets = desc.slcosmo.SLCosmo()
        Lets.make_some_mock_data(Nlenses=10, Nsamples=20)
        Lets.draw_some_prior_samples(Npriorsamples=100)
        Lets.compute_the_joint_log_likelihood()
        Lets.report_the_inferred_cosmological_parameters()
        Lets.plot_the_inferred_cosmological_parameters()
        H0, sigma = Lets.estimate_H0()
        lower_limit = H0 - 3.0*sigma
        upper_limit = H0 + 3.0*sigma
        self.assertGreater(Lets.cosmotruth['H0'], lower_limit)
        self.assertLess(Lets.cosmotruth['H0'], upper_limit)



if __name__ == '__main__':
    unittest.main()
