import os
import unittest
import desc.slcosmo

class TDC2ensembleTestCase(unittest.TestCase):
    def setUp(self):
        self.two_image_file = os.path.join(os.environ['SLCOSMO_DIR'], 'tests',
                                           'tdc2_2_image_ensemble.txt')
        self.four_image_file = os.path.join(os.environ['SLCOSMO_DIR'], 'tests',
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
        self.assertEqual(two_image.Nimages, 2)

        # Check for known sample size
        self.assertEqual(two_image.Nsamples, 1000)

        # Check for expected attributes for 2-image data.
        # @todo: Think about refactoring how DeltaFP* are handled.
        self.assertNotEqual(two_image.DeltaFP, None)
        self.assertNotEqual(two_image.DeltaFP_err, None)

        # Check that attributes for 4-image data are note present.
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AB, two_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AB_err, two_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AC, two_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AC_err, two_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AD, two_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_AD_err, two_image)

        # Tests for 4-image data.
        four_image = desc.slcosmo.TDC2ensemble.read_in_from(self.four_image_file)
        self.assertEqual(four_image.source, self.four_image_file)
        self.assertEqual(four_image.Nsamples, 1000)
        self.assertEqual(four_image.Nimages, 4)

        # Test for expected attributes.
        self.assertNotEqual(four_image.DeltaFP_AB, None)
        self.assertNotEqual(four_image.DeltaFP_AB_err, None)
        self.assertNotEqual(four_image.DeltaFP_AC, None)
        self.assertNotEqual(four_image.DeltaFP_AC_err, None)
        self.assertNotEqual(four_image.DeltaFP_AD, None)
        self.assertNotEqual(four_image.DeltaFP_AD_err, None)

        # Test that two-image attributes are not present.
        self.assertRaises(AttributeError, lambda x: x.DeltaFP, four_image)
        self.assertRaises(AttributeError, lambda x: x.DeltaFP_err, four_image)
