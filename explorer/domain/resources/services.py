import json
from pathlib import Path
import subprocess


def probe_mediafile_metadata(url: str) -> dict:
    """Uses ffmpeg to get some metadata over HTTP."""

    cmd = [
        'ffprobe',
        '-v',
        'error',
        '-show_entries',
        'format=format_name,format_long_name,duration,size,bit_rate',
        '-show_entries',
        'stream=index,codec_type,codec_name,width,height,r_frame_rate',
        '-of',
        'json',
        url,
    ]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return json.loads(result.stdout)


def format_to_media_type(format_name: str) -> tuple[str, str]:
    """
    Uses this map to get the media type from ffmpeg format output:
    https://gist.github.com/DusanBrejka/35238dccb5cefcc804de1c5a218ee004
    """
    with open(Path(__file__).parent / 'ffmpeg_format_to_media_type.json') as f:
        map = json.load(f)
        media_type = map[format_name]
        return tuple(media_type.split('/'))
