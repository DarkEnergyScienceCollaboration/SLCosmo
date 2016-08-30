import os
import numpy as np
import unittest
import desc.slcosmo

class TDC2ensembleTestCase(unittest.TestCase):
    def setUp(self):
        self.two_image_file = os.path.join(os.environ['SLCOSMO_DIR'],
                                           'tests',
                                           'tdc2_2_image_ensemble.txt')
        self.four_image_file = os.path.join(os.environ['SLCOSMO_DIR'],
                                           'tests',
                                           'tdc2_4_image_ensemble.txt')

    def tearDown(self):
        pass

    def test_read_in_from(self):
        """
        Tests TDC2ensemble.read_in_from for 2-image and 4-image files.
        """
        # Tests for 2-image data.
        two_image = desc.slcosmo.TDC2ensemble.read_in_from(self.two_image_file)
        self.assertEqual(two_image.source, self.two_image_file)
        self.assertEqual(two_image.Nim, 2)

        # Check for known sample size
        self.assertEqual(two_image.Nsamples, 20)

        # Check for expected attributes for 2-image data.
        self.assertEqual(len(two_image.DeltaFP_obs), 1)
        self.assertEqual(len(two_image.DeltaFP_err), 1)

        self.assertAlmostEqual(two_image.DeltaFP_obs[0], 885.602408386)
        self.assertAlmostEqual(two_image.DeltaFP_err[0], 34.0959154248)

        # Tests for 4-image data.
        four_image = desc.slcosmo.TDC2ensemble.read_in_from(self.four_image_file)
        self.assertEqual(four_image.source, self.four_image_file)
        self.assertEqual(four_image.Nsamples, 20)
        self.assertEqual(four_image.Nim, 4)
        self.assertEqual(len(four_image.DeltaFP_obs), 3)
        self.assertEqual(len(four_image.DeltaFP_err), 3)

        self.assertAlmostEqual(four_image.DeltaFP_obs[0], 1008.19147194)
        self.assertAlmostEqual(four_image.DeltaFP_err[0], 39.7134169074)
        self.assertAlmostEqual(four_image.DeltaFP_obs[1], 1150.72879342)
        self.assertAlmostEqual(four_image.DeltaFP_err[1], 45.348122074)
        self.assertAlmostEqual(four_image.DeltaFP_obs[2], 1088.08600626)
        self.assertAlmostEqual(four_image.DeltaFP_err[2], 42.0078296141)

    def test_read_write(self):
        """
        Test the consistency of an object created with .read_in_from
        with the original which persisted its state via .write_out_to.
        """
        two_image_temp_file = 'two_image_temp.txt'
        two_image = desc.slcosmo.TDC2ensemble.read_in_from(self.two_image_file)
        two_image.write_out_to(two_image_temp_file)
        temp_image = desc.slcosmo.TDC2ensemble.read_in_from(two_image_temp_file)
        self.assertEqual(two_image.DeltaFP_obs[0], temp_image.DeltaFP_obs[0])
        self.assertEqual(two_image.DeltaFP_err[0], temp_image.DeltaFP_err[0])
        self.assertTrue(np.allclose(two_image.dt_obs, temp_image.dt_obs))
        os.remove(two_image_temp_file)

        four_image_temp_file = 'four_image_temp.txt'
        four_image = desc.slcosmo.TDC2ensemble.read_in_from(self.four_image_file)
        four_image.write_out_to(four_image_temp_file)
        temp_image = desc.slcosmo.TDC2ensemble.read_in_from(four_image_temp_file)
        for i in range(3):
            self.assertEqual(four_image.DeltaFP_obs[i],
                             temp_image.DeltaFP_obs[i])
            self.assertEqual(four_image.DeltaFP_err[i],
                             temp_image.DeltaFP_err[i])
        self.assertTrue(np.allclose(four_image.dt_obs, temp_image.dt_obs))
        os.remove(four_image_temp_file)

if __name__ == '__main__':
    unittest.main()
