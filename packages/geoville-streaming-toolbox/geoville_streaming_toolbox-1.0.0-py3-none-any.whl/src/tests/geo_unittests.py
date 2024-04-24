# Basic Python Modules
import os
import json
import shutil
import unittest

# Third Party modules
from pyproj.crs import CRS

# Internal Modules
from src.lib.geo import execute_cmd, resample, reproject, tif_to_geotiff


class GeoUnitTests(unittest.TestCase):
    """
    Unit Tests of the geo functions
    """
    test_image = "src/tests/data/test_image.tif"
    test_image_crs = "epsg:3857"
    plain_image_path = "src/tests/data/test_plain_image.tif"

    def test_execute_cmd_success(self):
        """
        Test the successful execution of the function execute_cmd
        """

        try:
            execute_cmd("echo 'Hello World'")
        except ValueError:
            self.fail("execute_cmd raised an Exception unexpectedly!")

    def test_execute_cmd_failure(self):
        """
        Test the failure of executing the function execute_cmd with a non-
        existing command
        """

        self.assertRaises(Exception, execute_cmd, "whatever")

    def test_reproject_success(self):
        """
        Test the successful execution of gdalwarp for reprojection
        """
        test_reprojected_path = reproject(self.test_image_crs,
                                          "epsg:32628",
                                          10,
                                          self.test_image)

        # check the EPSG code of the result. Should be 32628
        try:
            gdalinfo_output = execute_cmd(f"gdalinfo {test_reprojected_path} "
                                          f"-json")
            gdalinfo_output = json.loads(gdalinfo_output)
            crs = CRS(gdalinfo_output["coordinateSystem"]["wkt"])
            epsg = crs.to_epsg()
        except json.decoder.JSONDecodeError as json_err:
            epsg = None
            print(f"Reprojection Test Failed - GdalInfo was not parsable: "
                  f"{json_err}")

        os.remove(test_reprojected_path)

        self.assertEqual(32628, epsg)

    def test_reproject_success_samePath(self):
        """
        Test the successful execution of gdalwarp for reprojection if the input
        projection equals the output projection. The resulting path should
        equal the input path
        """
        test_reprojected_path = reproject(self.test_image_crs,
                                          self.test_image_crs,
                                          10,
                                          self.test_image)

        self.assertEqual(self.test_image, test_reprojected_path)

    def test_reproject_failure_InputPathDoesNotExist(self):
        """
        Test the failure of the reprojection function if the input
        path does not exist
        """
        self.assertRaises(FileNotFoundError, reproject, self.test_image_crs,
                          "epsg:32632", 10, "src/tests/data/whatever_repr.tif")

    def test_reproject_failure_WrongParameter(self):
        """
        Test the failure of the reprojection function if an input
        parameter is wrong
        """
        self.assertRaises(ValueError, reproject, self.test_image_crs,
                          "epsg:whatever", 10, self.test_image)

    def test_resample_success(self):
        """
        Test the successful execution of gdalwarp for resampling
        """
        test_resampled_path = resample(10, 20, self.test_image)

        # check the resolution of the result. Should be 20
        try:
            gdalinfo_output = execute_cmd(f"gdalinfo {test_resampled_path} "
                                          f"-json")
            gdalinfo_output = json.loads(gdalinfo_output)
            geotransform = gdalinfo_output["geoTransform"]
            resolution = geotransform[1]
        except json.decoder.JSONDecodeError as json_err:
            resolution = None
            print(f"Resampling Test Failed - GdalInfo was not parsable: "
                  f"{json_err}")

        os.remove(test_resampled_path)

        self.assertEqual(20, resolution)

    def test_resample_success_samePath(self):
        """
        Test the successful execution of gdalwarp for resampling if the input
        resolution equals the output resolution. The resulting path should
        equal the input path
        """
        test_resampled_path = resample(10, 10, self.test_image)

        self.assertEqual(self.test_image, test_resampled_path)

    def test_resample_failure_InputPathDoesNotExist(self):
        """
        Test the failure of the resampling function if the input
        path does not exist
        """
        self.assertRaises(FileNotFoundError, resample, 10, 20,
                          "src/tests/data/whatever_res.tif")

    def test_resample_failure_WrongParameter(self):
        """
        Test the failure of the resampling function if an input
        parameter is wrong
        """
        self.assertRaises(ValueError, resample, 10, "whatever",
                          self.test_image)

    def test_tif_to_geotiff_success(self):
        """
        Test the successful execution of gdal_edit.py for converting a Tiff to
        a GeoTiff
        """
        plain_temporary_image_path = "src/tests/data/test_plain_image_tmp.tif"

        # copy the plain image, because its metadata gets overwritten
        shutil.copyfile(self.plain_image_path, plain_temporary_image_path)

        tif_to_geotiff(plain_temporary_image_path, self.test_image_crs,
                       (262830, 6337050, 262930, 6337150))

        # check the resolution and the projection of the result.
        # Should be 10 meters and EPSG:3857
        try:
            gdalinfo_output = execute_cmd(f"gdalinfo "
                                          f"{plain_temporary_image_path} "
                                          f"-json")
            gdalinfo_output = json.loads(gdalinfo_output)
            geotransform = gdalinfo_output["geoTransform"]
            resolution = geotransform[1]
            crs = CRS(gdalinfo_output["coordinateSystem"]["wkt"])
            epsg = crs.to_epsg()
        except json.decoder.JSONDecodeError as json_err:
            resolution = None
            epsg = None
            print(f"tif_to_geotiff Test Failed - GdalInfo was not parsable: "
                  f"{json_err}")

        os.remove(plain_temporary_image_path)

        self.assertEqual((10, 3857), (resolution, epsg))

    def test_tif_to_geotiff_failure_InputPathDoesNotExist(self):
        """
        Test the failure of gdal_edit.py for converting a Tiff to
        a GeoTiff by providing a non-existing input path
        """
        self.assertRaises(FileNotFoundError, tif_to_geotiff,
                          "src/tests/data/whatever.tif", self.test_image_crs,
                          (262830, 6337050, 262930, 6337150))

    def test_tif_to_geotiff_failure_WrongProjParameter(self):
        """
        Test the failure of gdal_edit.py for converting a Tiff to
        a GeoTiff by providing a wrong projection
        """
        self.assertRaises(ValueError, tif_to_geotiff,
                          self.plain_image_path,
                          "epsg:whatever",
                          (262830, 6337050, 262930, 6337150))

    def test_tif_to_geotiff_failure_WrongExtentParameter(self):
        """
        Test the failure of gdal_edit.py for converting a Tiff to
        a GeoTiff by providing a wrong extent
        """
        self.assertRaises(ValueError, tif_to_geotiff,
                          "src/tests/data/test_plain_image.tif",
                          self.test_image_crs,
                          (262830, 6337050, 262930))
