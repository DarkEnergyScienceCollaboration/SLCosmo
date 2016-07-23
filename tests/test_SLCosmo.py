"""
Example unit tests for SLCosmo package
"""
import unittest
import desc.slcosmo

class SLCosmoTestCase(unittest.TestCase):

    def setUp(self):
        self.message = 'Testing SLCosmo...'

    def tearDown(self):
        pass

    # ------------------------------------------------------------------
    # Unit tests:

    def test_factory(self):
        Lets = desc.slcosmo.SLCosmo()
        Lets.make_some_mock_data(3)
        self.assertEquals(len(Lets.lenses), 3)

    def test_read_in_time_delay_samples(self):
        Lets = desc.slcosmo.SLCosmo()
        Lets.make_some_mock_data(1)
        Lets.read_in_time_delay_samples(['mock_time_delays_0.txt'])
        self.assertEquals(Lets.Nlenses, 1)
        # BUG: THIS TEST IS PRETTY MEANINGLESS

    # ------------------------------------------------------------------
    # Scientific tests:

    def test_round_trip(self):
        Lets = desc.slcosmo.SLCosmo()
        Lets.make_some_mock_data(Nlenses=40, Nsamples=100)
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
