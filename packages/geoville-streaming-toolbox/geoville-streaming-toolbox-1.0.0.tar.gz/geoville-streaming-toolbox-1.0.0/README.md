![](logo.png)

---
**Author:** Johannes Schmid  
**Version:** 22.3 
---

This repository contains the code for extracting
time frames from online accessible satellite streams.  

Via an API the streams and meta information will be retrieved. After 
extracting the desired image frames for an area of interest, the Tiff files 
will be converted to GeoTiff files containing all geographical information 
such as the coordinate reference system and the geo-transformation. If 
required the projection and the resolution can be adapted as well.

## Usage:

    usage: main.py [-h] -i INPUT -o OUTPUT [-b BAND] -s START -e END -m MISSION [-p PROJECTION] [-r RESOLUTION]
    
    Download satellite images of a desired time frame and area of interest from online streams.
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --Input INPUT
                            Path to a GeoJson including the Area of Interest. Note that a GeoJson always has to have the projection EPSG:4326!
      -o OUTPUT, --Output OUTPUT
                            Path to the output directory.
      -b BAND, --Band BAND  Input band number (e.g. B04)
      -s START, --Start START
                            Start Date (e.g. 2021-01-15)
      -e END, --End END     End Date (e.g. 2021-01-31)
      -m MISSION, --Mission MISSION
                            Satellite mission (e.g. S1, S2, etc.
      -p PROJECTION, --Projection PROJECTION
                            Output projection (EPSG, WKT or Proj4)
      -r RESOLUTION, --Resolution RESOLUTION
                            Resolution in meters (e.g. 10, 20, etc.)

## Example Call:

The following command will download Sentinel 2 (S2) images from 2018-02-01 
until 2018-05-01 for the region that is specified in the input GeoJson 
(/test.geojson). Since Band 4 was specified (B04), only this band will be 
downloaded to the output directory (/test_output). Moreover, a projection 
(epsg:3857) and a resolution were defined, so the output will be reprojected 
and resampled accordingly.

`python3 main.py -i /test.geojson -o /test_output -m S2 -b B04 
-s 2018-02-01 -e 2018-05-01 -p epsg:3857 -r 20`

For using the module without Docker, the requirements can be installed as follows:  
`pip install -r requirements.txt`  
Please make sure that  you provide the path to the requirements.txt file in case you are outside the repository.  
Besides the python modules of the requirements.txt, make sure that GDAL 3.4.1 (released 2021/12/27) is installed.  
  
  
Using **Docker**, the example call would look as follows:

`docker run -v /home/user/Desktop:/out fas_data_access /bin/bash -c 
"python3 main.py -i /src/tests/data/test.geojson -o /out/test_output -b B04 
-s 2018-02-01 -e 2018-02-15 -m S2"`

Since the directory */home/user/Desktop* was mounted to */*, the 
output directory lies at */home/user/Desktop*.

Please also note that the Docker image in this example is called 
*fas_data_access*. In order to create this image, switch to the repository 
directory and execute the following command.

`docker build -t fas_data_access .`  
  
You can also pull this image from Dockerhub via  
`docker pull geoville/csc_streamer_toolbox_demo`  
  

## Requirements:  
The module was created and tested with **16 GB RAM and a 32 GB Swapfile**.  
Please make sure to use this module on a system with similar or higher memory specifications.  