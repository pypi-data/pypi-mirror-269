"""
This script contains the main code and shows all steps for extracting
time frames from online accessible satellite streams. Via an API the streams
and meta information will be retrieved. After extracting images of the
specified time frame and area of interest, the Tiff files will be upgraded to
GeoTiff files containing all geographical information such as the coordinate
reference system and the geo-transformation. If required the projection and
the resolution can be adapted as well.
"""

__author__ = "Johannes Schmid"
__copyright__ = "GeoVille Information Systems GmbH"
__license__ = "MIT"
__version__ = "22.3"
__maintainer__ = "Johannes Schmid"
__email__ = "schmid@geoville.com"
__status__ = "Production"

# Basic Python Modules
import os
import json
import argparse
from glob import glob

# Internal Modules
from lib.api import request_streams, reform_response
from lib.stream import get_metadata, extract_images
from lib.geo import tif_to_geotiff, reproject, resample
from lib.general import read_config, temporary_to_final


if __name__ == '__main__':

    # Parser ==================================================================
    parser = argparse.ArgumentParser(
        description='Download satellite images of a desired time frame and '
                    'area of interest from online streams.')
    parser.add_argument("-i", "--Input", type=str, required=True,
                        help="Path to a GeoJson including the Area of "
                             "Interest. Note that a GeoJson always has to "
                             "have the projection EPSG:4326!")
    parser.add_argument("-o", "--Output", type=str, required=True,
                        help="Path to the output directory.")
    parser.add_argument("-b", "--Band", type=str, required=False,
                        default="ALL", help="Input band number (e.g. B04)")
    parser.add_argument("-s", "--Start", type=str, required=True,
                        help="Start Date (e.g. 2021-01-15)")
    parser.add_argument("-e", "--End", type=str, required=True,
                        help="End Date (e.g. 2021-01-31)")
    parser.add_argument("-m", "--Mission", type=str, required=True,
                        help="Satellite mission (e.g. S1, S2, etc.")
    parser.add_argument("-p", "--Projection", type=str, required=False,
                        help="Output projection (EPSG, WKT or Proj4)")
    parser.add_argument("-r", "--Resolution", type=int, required=False,
                        help="Resolution in meters (e.g. 10, 20, etc.)")
    args = parser.parse_args()

    # Read permanent config variables =========================================
    tmp, band_info = read_config('config/config.yaml',
                                 args.Mission,
                                 args.Band)

    # Read the GeoJson ========================================================
    if not os.path.exists(args.Input):
        raise FileNotFoundError(f"Your GeoJson input {args.Input} "
                                f"does not exist.")

    with open(args.Input) as json_file:
        geojson = json.load(json_file)

    # API Request for streams =================================================
    response = request_streams(geojson,
                               args.Mission,
                               band_info["request"],
                               args.Start,
                               args.End)

    # Reform the response =====================================================
    streams = reform_response(response)

    # Loop through the streams ================================================
    for sid, (stream, stream_info) in enumerate(streams.items()):
        print(stream)

        # Create a temporary directory for each stream ------------------------
        tmp_dir = os.path.join(tmp["directory"], str(sid))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        # Parse the stream info -----------------------------------------------
        frames = (min(stream_info["image_number"]),
                  max(stream_info["image_number"]) + 1)
        tile_id = stream_info["tile_id"]
        crs = stream_info["crs"]
        extent = stream_info["bbox"]

        # Read metadata from the stream ---------------------------------------
        plane_type, number_frames = get_metadata(stream, frames)

        # Extract Tiffs from the stream ---------------------------------------
        plane = band_info[plane_type]
        plane = None if plane == 'None' else plane
        extract_images(stream,
                       os.path.join(tmp_dir, tmp["extraction_filename"]),
                       frames,
                       plane)

        # Loop through extracted images and their sensing-times ---------------
        extracted_images = sorted(glob(os.path.join(tmp_dir, "*.tif")))

        for extracted_image, sensing_time in zip(extracted_images,
                                                 stream_info["sensing_time"]):
            print(sensing_time)

            # Tiff to Geotiff .................................................
            output_tmp_path = tif_to_geotiff(extracted_image,
                                             crs,
                                             extent)

            # Reprojection ....................................................
            output_tmp_path = reproject(crs,
                                        args.Projection,
                                        band_info["res"],
                                        output_tmp_path)

            # Resampling ......................................................
            output_tmp_path = resample(band_info["res"],
                                       args.Resolution,
                                       output_tmp_path)

            # Move final output from the tmp- to the output-directory .........
            temporary_to_final(output_tmp_path,
                               args.Output,
                               args.Mission,
                               "_".join(band_info["request"]),
                               tile_id,
                               sensing_time)
