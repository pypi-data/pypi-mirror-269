# Basic Python Modules
import os
import unittest

# Third Party modules
import ffmpeg

# Internal Modules
from src.lib.stream import extract_images, get_metadata


class StreamUnitTests(unittest.TestCase):
    """
    Unit Tests of the ffmpeg stream functions
    """
    extracted_image_path = 'extraction_%03d.tif'

    def test_extract_images_success(self):
        """
        Test the successful extraction of a stream
        """

        extract_images('https://base-n.de/webm/out9.webm',
                       self.extracted_image_path,
                       (0, 1),
                       "y")
        self.assertTrue(os.path.exists('extraction_001.tif'))

    def test_extract_images_success_withoutPlane(self):
        """
        Test the successful extraction of a stream without a plane
        """

        extract_images('https://base-n.de/webm/out9.webm',
                       self.extracted_image_path,
                       (0, 1),
                       None)
        self.assertTrue(os.path.exists('extraction_001.tif'))

    def test_extract_images_failure_wrongPlane(self):
        """
        Test the failure of extracting a stream by providing a wrong plane
        """

        self.assertRaises(ffmpeg.Error, extract_images,
                          'https://csc-streamlined.'
                          'geoville.com/data/'
                          '28PCT_B08_B04_B03_'
                          '2018_1_UTM.webm',
                          self.extracted_image_path,
                          (0, 1),
                          "x")

    def test_extract_images_failure_wrongPath(self):
        """
        Test the failure of extracting a stream by providing a wrong path
        """

        self.assertRaises(ffmpeg.Error, extract_images,
                          'https://csc-whatever-streamlined.'
                          'geoville.com/data/'
                          '28PCT_B08_B04_B03_'
                          '2018_1_UTM.webm',
                          self.extracted_image_path,
                          (0, 1),
                          "r")

    def test_get_metadata_success(self):
        """
        Test the successful parsing of a stream's metadata
        """
        plane_type, number_frames = get_metadata('https://csc-streamlined.'
                                                 'geoville.com/data/'
                                                 '28PCT_B08_B04_B03_'
                                                 '2018_1_UTM.webm',
                                                 (0, 1))
        self.assertEqual(("rgb", 20), (plane_type, number_frames))

    def test_get_metadata_failure_wrongPath(self):
        """
        Test the failure of parsing of a stream's metadata by providing a wrong
        path
        """
        self.assertRaises(ffmpeg.Error, get_metadata,
                          'https://csc-whatever-streamlined.geoville.com/data/'
                          '28PCT_B08_B04_B03_2018_1_UTM.webm',
                          (0, 1))

    def test_get_metadata_failure_wrongFrames(self):
        """
        Test the failure of parsing of a stream's metadata by providing wrong
        frame numbers
        """
        self.assertRaises(IndexError, get_metadata,
                          'https://csc-streamlined.geoville.com/data/'
                          '28PCT_B08_B04_B03_2018_1_UTM.webm',
                          (10000, 100000))
