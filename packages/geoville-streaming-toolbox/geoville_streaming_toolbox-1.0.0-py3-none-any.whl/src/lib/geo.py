# Basic Python Modules
import os
import subprocess as sp


def execute_cmd(cmd):
    """
    Executes a command on the commandline

    :param cmd: command
    :type cmd: str
    """
    process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    out, err = process.communicate()
    if process.returncode != 0:
        raise ValueError('CMD ({}) failed with: {}'.format(cmd, str(err)))
    return out


def reproject(in_proj, out_proj, res, in_path):
    """
    Execution of GDAL's commandline gdalwarp to reproject a GeoTiff.
    :param in_proj: source projection
    :type in_proj: str
    :param out_proj: target projection
    :type out_proj: str
    :param res: target resolution
    :type res: int
    :param in_path: input file path (GeoTiff)
    :type in_path: str
    :return: output file path (GeoTiff). Equals in_path if in_proj = out_proj
    :rtype: str
    """
    out_path = in_path.replace(".tif", "_reprojected.tif")

    if not os.path.exists(in_path):
        raise FileNotFoundError(f"{in_path} does not exist.")

    if out_proj and out_proj != in_proj:
        cmd = f"gdalwarp -t_srs {out_proj} -tr {res} {res} " \
              f"{in_path} {out_path} -overwrite"
        execute_cmd(cmd)
        return out_path
    else:
        return in_path


def resample(in_res, out_res, in_path):
    """
    Execution of GDAL's commandline gdalwarp to resample a GeoTiff.
    :param in_res: source resolution
    :type in_res: int
    :param out_res: target resolution
    :type out_res: int
    :param in_path: input file path (GeoTiff)
    :type in_path: str
    :return: output file path (GeoTiff). Equals in_path if in_proj = out_proj
    :rtype: str
    """

    if not os.path.exists(in_path):
        raise FileNotFoundError(f"{in_path} does not exist.")

    out_path = in_path.replace(".tif", f"_{out_res}m.tif")
    if out_res and out_res != in_res:
        cmd = f"gdalwarp -tr {out_res} {out_res} " \
              f"{in_path} {out_path} -overwrite"
        execute_cmd(cmd)
        return out_path
    else:
        return in_path


def tif_to_geotiff(in_path, crs, extent):
    """
    Execution of GDAL's python script gdal_edit.py to add geo-information to
     an input Tiff file. The result is a GeoTiff.
    :param in_path: input file path (GeoTiff)
    :type in_path: str
    :param crs: coordinate reference system (EPSG, WKT or Proj4)
    :type crs: str
    :param extent: xmin, ymin, xmax, ymax coordinates
    :type extent: tuple
    :return: in_path
    :rtype: str
    """

    if not os.path.exists(in_path):
        raise FileNotFoundError(f"{in_path} does not exist.")

    xmin, ymin, xmax, ymax = extent
    cmd = f"gdal_edit.py -a_srs {crs} " \
          f"-a_ullr {xmin} {ymax} {xmax} {ymin} {in_path}"
    execute_cmd(cmd)
    return in_path
