"""
Unit tests for SLCosmo class
"""
import unittest
import desc.slcosmo

class SLCosmoUnitTestCase(unittest.TestCase):

    def setUp(self):
        self.message = 'Testing SLCosmo...'

    def tearDown(self):
        pass

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


if __name__ == '__main__':
    unittest.main()
