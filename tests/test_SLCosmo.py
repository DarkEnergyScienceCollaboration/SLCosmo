"""
Example unit tests for SLCosmo package
"""
import unittest
import desc.slcosmo

class SLCosmoTestCase(unittest.TestCase):
    def setUp(self):
        self.message = 'Hello, world'
        
    def tearDown(self):
        pass

    def test_read_in_time_delays(self):
        foo = desc.slcosmo.SLCosmo(self.message)
        self.assertEquals(foo.read_in_time_delays(), self.message)

    def test_failure(self):
        self.assertRaises(TypeError, desc.slcosmo.SLCosmo)
        foo = desc.slcosmo.SLCosmo(self.message)
        self.assertRaises(RuntimeError, foo.read_in_time_delays, True)

if __name__ == '__main__':
    unittest.main()
