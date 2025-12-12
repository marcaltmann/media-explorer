"""
ffmpeg commands as Python functions.
"""

import subprocess
import tempfile


def generate_thumbnail(video_url: str, position: int = 5, width: int = 320) -> str:
    """
    Generate a single thumbnail from a video.

    Args:
        video_url: URL of input video
        position: Time to extract frame (format: seconds)
        width: Thumbnail width
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
    temp_path = temp_file.name
    temp_file.close()  # Close it so ffmpeg can write to it

    # fmt: off
    cmd = [
        'ffmpeg',
        '-ss', str(position),              # set the start time offset
        '-accurate_seek',                  # enable/disable accurate seeking with -ss
        '-i', video_url,                   # infile
        '-vframes', '1',                   # set the number of video frames to record
        '-vf', f'scale={width}:-1',        # set video filters
        '-y',                              # overwrite output files
        temp_path
    ]
    # fmt: on

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f'Generated: {temp_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error generating thumbnail: {e.stderr}')
        raise

    return temp_path
