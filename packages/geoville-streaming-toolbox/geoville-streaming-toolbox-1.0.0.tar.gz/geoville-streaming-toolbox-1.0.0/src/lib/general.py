# Basic Python Modules
import os
import shutil

# Third Party modules
import yaml


def temporary_to_final(output_tmp_path, output_directory, mission, bands,
                       tile_id, sensing_time):
    """
    This function copies the final output from the temporary to the desired
    output directory.
    :param output_tmp_path: temporary output path
    :type output_tmp_path: str
    :param output_directory: final output directory defined by the user
    :type output_directory: str
    :param mission: mission of the output
    :type mission: str
    :param bands: satellite bands of the output
    :type bands: str
    :param tile_id: satellite tile id of the output
    :type tile_id: str
    :param sensing_time: sensing time of the output
    :type sensing_time: str
    """

    output_filename = f"{mission}_{tile_id}_{bands}_{sensing_time}.tif"
    output_path = os.path.join(output_directory, output_filename)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not output_tmp_path.endswith(".tif"):
        raise TypeError(f"You try to copy an output that does not seem to be "
                        f"a GeoTiff: {output_tmp_path}")

    if not os.path.exists(output_tmp_path):
        raise FileNotFoundError(f"Your temporary output file "
                                f"{output_tmp_path} does not exist.")

    shutil.copyfile(output_tmp_path, output_path)


def read_config(config_path, mission, band):
    """
    Reading and parsing of the config file
    :param config_path: path to the config yaml-file
    :type config_path: str
    :param mission: satellite mission the user desires
    :type mission: str
    :param band: satellite band the user desires
    :type band: str
    :return: configuration of the temporary paths and the satellite band info
    :rtype: (dict, dict)
    """

    with open(config_path) as file:
        cfg = yaml.load(file, Loader=yaml.FullLoader)

    tmp = cfg["tmp"]

    try:
        band_info = cfg["band_info"][mission][band]
    except KeyError:
        raise KeyError("The satellite mission or band of your request "
                       "is not implemented yet.")

    return tmp, band_info
