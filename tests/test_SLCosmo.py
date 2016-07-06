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

    def test_run(self):
        foo = desc.slcosmo.SLCosmo(self.message)
        self.assertEquals(foo.run(), self.message)

    def test_failure(self):
        self.assertRaises(TypeError, desc.slcosmo.SLCosmo)
        foo = desc.slcosmo.SLCosmo(self.message)
        self.assertRaises(RuntimeError, foo.run, True)

if __name__ == '__main__':
    unittest.main()
