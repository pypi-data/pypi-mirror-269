# Basic Python Modules
import json
import unittest

# Third Party modules
import requests

# Internal Modules
from src.lib.api import request_streams, reform_response


class APIUnitTests(unittest.TestCase):
    """
    Unit Tests of the API functions
    """
    geojson_path = "src/tests/data/test.geojson"
    stream_path = 'https://csc-streamlined.geoville.com/data/' \
                  '28PCT_B08_B04_B03_2018_1_UTM.webm'

    def test_request_streams_success(self):
        """
        Test the successful request of a stream
        """

        with open(self.geojson_path) as json_file:
            geojson = json.load(json_file)

        response = request_streams(geojson,
                                   "S2",
                                   ["B04", "B03", "B08"],
                                   "2018-02-01",
                                   "2018-02-04")

        expected_response = {'data': [{'tile_id': '28PCT',
                                       'obs_year': 2018,
                                       'image_number': 12,
                                       'sensing_time': '2018_02_02T11:37:55',
                                       'stream_path': 'data.csc-streamlined.geoville.com/28PCT_B08_B04_B03_2018_1_UTM.webm',
                                       'cloudy_pixel_percentage': 70.37637,
                                       'nodata_pixel_percentage': 67.29533,
                                       'crs': 'EPSG:32628',
                                       'bbox': [299999.9999639829,
                                        1190219.9999550516,
                                        409799.99996602884,
                                        1300020.000024519]},
                                      {'tile_id': '28PCT',
                                       'obs_year': 2018,
                                       'image_number': 13,
                                       'sensing_time': '2018_02_04T11:30:25',
                                       'stream_path': 'data.csc-streamlined.geoville.com/28PCT_B08_B04_B03_2018_1_UTM.webm',
                                       'cloudy_pixel_percentage': 99.7725,
                                       'nodata_pixel_percentage': 9.359408,
                                       'crs': 'EPSG:32628',
                                       'bbox': [299999.9999639829,
                                        1190219.9999550516,
                                        409799.99996602884,
                                        1300020.000024519]}]}

        self.assertEqual(expected_response, response)

    def test_request_streams_failure_wrongParameter(self):
        """
        Test the failure of the request of a stream by providing a wrong API
        payload
        """

        with open(self.geojson_path) as json_file:
            geojson = json.load(json_file)

        self.assertRaises(requests.exceptions.HTTPError,
                          request_streams, geojson, "S1",
                          ["B04", "B03", "B08"], "2018-02-01", "2018-02-04")

    def test_request_streams_failure_missingParameter(self):
        """
        Test the failure of the request of a stream with a missing one payload
        parameter
        """

        with open(self.geojson_path) as json_file:
            geojson = json.load(json_file)

        self.assertRaises(requests.exceptions.HTTPError,
                          request_streams, geojson, None,
                          ["B04", "B03", "B08"], "2018-02-01", "2018-02-04")

    def test_reform_response_success(self):
        """
        Test the success of reforming the API response
        """
        test_response = {'data': [
            {'bbox': [299999.9999639829,
                      1190219.9999550516,
                      409799.99996602884,
                      1300020.000024519],
             'cloudy_pixel_percentage': 70.37637,
             'crs': 'EPSG:32628',
             'image_number': 12,
             'nodata_pixel_percentage': 67.29533,
             'obs_year': 2018,
             'sensing_time': '2018_02_02T11:37:55',
             'stream_path': self.stream_path,
             'tile_id': '28PCT'},
            {'bbox': [299999.9999639829,
                      1190219.9999550516,
                      409799.99996602884,
                      1300020.000024519],
             'cloudy_pixel_percentage': 99.7725,
             'crs': 'EPSG:32628',
             'image_number': 13,
             'nodata_pixel_percentage': 9.359408,
             'obs_year': 2018,
             'sensing_time': '2018_02_04T11:30:25',
             'stream_path': self.stream_path,
             'tile_id': '28PCT'}
        ]}

        reformed_test_response = reform_response(test_response)

        expected_reformed_response = \
            {'https://csc-streamlined.geoville.com/data/'
             '28PCT_B08_B04_B03_2018_1_UTM.webm':
                 {'tile_id': '28PCT',
                  'crs': 'EPSG:32628',
                  'bbox': [299999.9999639829, 1190219.9999550516,
                           409799.99996602884, 1300020.000024519],
                  'image_number': [12, 13],
                  'sensing_time': ['2018_02_02T11:37:55',
                                   '2018_02_04T11:30:25']}
             }

        self.assertEqual(expected_reformed_response, reformed_test_response)

    def test_reform_response_failure(self):
        """
        Test the failure of reforming the API response that does not look as
         expected. This might occur if the API repsonse changes
        """
        unexpected_test_response = {'data': [
            {
             'cloudy_pixel_percentage': 70.37637,
             'crs': 'EPSG:32628',
             'image_number': 12,
             'nodata_pixel_percentage': 67.29533,
             'obs_year': 2018,
             'sensing_time': '2018_02_02T11:37:55',
             'stream_path': self.stream_path,
             'tile_id': '28PCT'},
            {
             'cloudy_pixel_percentage': 99.7725,
             'crs': 'EPSG:32628',
             'image_number': 13,
             'nodata_pixel_percentage': 9.359408,
             'obs_year': 2018,
             'sensing_time': '2018_02_04T11:30:25',
             'stream_path': self.stream_path,
             'tile_id': '28PCT'}
        ]}

        self.assertRaises(KeyError, reform_response, unexpected_test_response)
