# Basic Python Modules
from datetime import datetime as dt

# Third Party modules
import ffmpeg


def get_metadata(in_file, frames):
    """
    Parse metadata from a stream by using the probe functionality of ffmpeg
    :param in_file: input file path or url
    :type in_file: str
    :param frames: start and end frame
    :type frames: tuple
    :return: plane type (pixel format) of the stream (e.g. rgb or yuv) \
     and the number of frames within the input stream
     :rtype: (str, int)
    """

    # use ffmpeg.probe to parse the stream information
    try:
        probe = ffmpeg.probe(in_file)
    except ffmpeg.Error as e:
        print(e.stderr.decode('utf8'))
        raise e

    # extract only the necessary video information from the stream information
    video_info = next(s
                      for s in probe['streams'] if s['codec_type'] == 'video')

    # get the plane type (e.g. rgb or yuv)
    if "gbr" in video_info["pix_fmt"]:
        plane_type = "rgb"
    elif "yuv" in video_info["pix_fmt"]:
        plane_type = "yuv"
    else:
        plane_type = video_info["pix_fmt"][:3]

    # calculate the stream duration in seconds
    duration = (dt.strptime(video_info['tags']['DURATION'][:-3],
                            '%H:%M:%S.%f') - dt(1900, 1, 1)).total_seconds()

    # get the number of frames of the stream
    number_frames = int(duration * 4)

    # raise an error if the required frames fall outside the stream frames
    if frames[0] > number_frames or frames[1] > number_frames:
        raise IndexError(f"Frame needs to be between 0 and {number_frames}. "
                         f"However, you requested the frames "
                         f"{frames[0]} - {frames[1]}.")

    return plane_type, number_frames


def extract_images(in_file, out_file, frames, plane):
    """
    Extract frames/images from a stream using ffmpeg
    :param in_file: input file path or url
    :type in_file: str
    :param out_file: output file path including a pattern (e.g. %03d) so that \
    each output file includes the frame number.
    :type out_file: str
    :param frames: start and end frame
    :type frames: tuple
    :param plane: desired band, written in the pixel format of the stream \
    (e.g. "r" as first band of a "rgb" image)
    :type plane: Union[str, None]
    """

    start_frame, end_frame = frames

    try:
        # 1. read the input file or url
        step1_read_ffmpeg = ffmpeg.input(in_file)

        # 2. trim the stream using a start and end frame
        step2_filter_frames = step1_read_ffmpeg.trim(start_frame=start_frame,
                                                     end_frame=end_frame)

        # 3. if required, use 'extractplanes' to filter for a specific band
        if plane:
            step3_filter_plane = step2_filter_frames.filter('extractplanes',
                                                            plane)
        else:
            step3_filter_plane = step2_filter_frames

        # 4. define the output format and path
        step4_write_tif = \
            step3_filter_plane.output(out_file,
                                      format='image2',
                                      vcodec='tiff').overwrite_output()

        # execute all ffmpeg steps (1-4)
        step4_write_tif.run(capture_stdout=True, capture_stderr=True)

    except ffmpeg.Error as e:
        print(e.stderr.decode('utf8'))
        raise e
