# Third Party modules
import requests


def request_streams(geojson, mission, bands, start_date, end_date):
    """
    POST-Request of the CSC-API to obtain the stream url's and further metadata
    :param geojson: Json including the area of interest (GeoJson).
    :type geojson: dict
    :param mission: Satellite mission (e.g. S1, S2, etc.)
    :type mission: str
    :param bands: List of satellite bands
    :type bands: list
    :param start_date: start date (e.g. 2021-01-15)
    :type start_date: str
    :param end_date: end date (e.g. 2021-01-31)
    :type end_date: str
    :return: API response
    :rtype: dict
    """
    endpoint = "https://api.csc-streamlined.geoville.com/streaming/products"

    payload = {"start_date": start_date,
               "end_date": end_date,
               "mission": mission,
               "bands": bands,
               "geoJSON": geojson}

    try:
        response = requests.post(url=endpoint, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"Requesting streams failed with "
                                            f"{e.response.text}")

    return response.json()


def reform_response(response):
    """
    Rearrangement of the CSC-API response.
    :param response: CSC-API response
    :type response: dict
    :return: rearranged dictionary with the stream url's as keys
    :rtype: dict
    """

    # INPUT
    # {"data": [
    #                 {"tile_id": "28PCT",
    #                 "obs_year": 2017,
    #                 "image_number": 0,
    #                 "sensing_time": "2017-01-15...",
    #                 "stream_path": "http://....",
    #                 "cloudy_pixel_percentage": 0,
    #                 "nodata_pixel_percentage": 0,
    #                 "crs": "epsg:32628",
    #                 "bbox": [1, 2, 3, 4]}
    #             , ....]
    # }

    # OUTPUT
    # {"http:...": {"tile_id": "28PCT"
    #               "crs": "epsg:32628",
    #               "bbox": [1, 2, 3, 4],
    #               "image_number": [0, 1],
    #               "sensing_time": ["2017-01-15...", "2017-01-20..."]}
    #  , ...}

    streams = {}

    for element in response["data"]:

        # if the stream url does not exist as key of the 'streams' variable,
        # insert it with an empty dictionary as value.
        if element["stream_path"] not in streams:
            streams[element["stream_path"]] = {}

        # add static elements (tile id, crs, bbox) as items to the
        # stream url value
        for static_element in ["tile_id", "crs", "bbox"]:
            if static_element not in streams[element["stream_path"]]:
                streams[element["stream_path"]][static_element] \
                    = element[static_element]

        # add list for the image_number and the sensing_time in case
        # they do not exist within the stream url value, otherwise append their
        # content to the list.
        for list_element in ["image_number", "sensing_time"]:
            if list_element not in streams[element["stream_path"]]:
                streams[element["stream_path"]][list_element] = \
                    [element[list_element]]
            else:
                streams[element["stream_path"]][list_element]. \
                    append(element[list_element])

    return streams
