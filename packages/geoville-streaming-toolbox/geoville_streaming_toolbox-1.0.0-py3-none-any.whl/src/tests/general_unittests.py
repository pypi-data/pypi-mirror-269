# Basic Python Modules
import unittest

# Internal Modules
from src.lib.general import temporary_to_final, read_config


class GeneralUnitTests(unittest.TestCase):
    """
    Unit Tests of the general functions
    """
    output_directory = "/src"
    config_path = 'src/config/config.yaml'

    def test_temporary_to_final_success(self):
        """
        Test the successful execution of the function temporary_to_final
        """

        output_tmp_path = "src/tests/data/test_image.tif"
        mission = "S2"
        sensing_time = "2018_02_02T11:37:55"
        bands = "B04_B03_B08"
        tile_id = "28PCT"

        try:
            temporary_to_final(output_tmp_path,
                               self.output_directory,
                               mission,
                               bands,
                               tile_id,
                               sensing_time)
        except (FileNotFoundError, TypeError, PermissionError):
            self.fail("temporary_to_final raised an Exception unexpectedly!")

    def test_temporary_to_final_failure_FileNotExists(self):
        """
        Test the failure of the execution of the function temporary_to_final
        due to a non-existing temporary output file path
        """

        output_tmp_path = "src/tests/data/whatever.tif"
        mission = "S2"
        sensing_time = "2018_02_02T11:37:55"
        bands = "B04_B03_B08"
        tile_id = "28PCT"

        self.assertRaises(FileNotFoundError,
                          temporary_to_final,
                          output_tmp_path, self.output_directory, mission,
                          bands, tile_id, sensing_time)

    def test_temporary_to_final_failure_NoGeotiff(self):
        """
        Test the failure of the execution of the function temporary_to_final
        due to a temporary output file path with the wrong data format
        """

        output_tmp_path = "src/tests/data/test.geojson"
        mission = "S2"
        sensing_time = "2018_02_02T11:37:55"
        bands = "B04_B03_B08"
        tile_id = "28PCT"

        self.assertRaises(TypeError,
                          temporary_to_final,
                          output_tmp_path, self.output_directory, mission,
                          bands, tile_id, sensing_time)

    def test_read_config_success_tmpKeys(self):
        """
        Test the reading of the config file and that the tmp section within the
        configuration stays as expected
        """
        tmp, _ = read_config(self.config_path, "S2", "B04")

        expected_tmp_keys = ["directory", "extraction_filename"]

        self.assertEqual(expected_tmp_keys, list(tmp.keys()))

    def test_read_config_success_bandInfoKeys(self):
        """
        Test the reading of the config file and that the band info structure
        within the configuration stays as expected
        """
        _, band_info = read_config(self.config_path, "S2", "B04")

        expected_tmp_keys = ["res", "rgb", "yuv", "request"]

        self.assertEqual(expected_tmp_keys, list(band_info.keys()))

    def test_read_config_failure_FileNotExists(self):
        """
        Test the failure of reading a config file that does not exist
        """
        self.assertRaises(FileNotFoundError, read_config,
                          'whatever/config.yaml', "S2", "B04")

    def test_read_config_failure_KeyMissing(self):
        """
        Test the failure of requesting non-existing keys from the config file
        """
        self.assertRaises(KeyError, read_config,
                          self.config_path, "S9", "B04")
