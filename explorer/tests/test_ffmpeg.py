from explorer.domain.resources.services import format_to_media_type

def test_format_to_media_type():
    """Gets media type as a tuple from ffmpeg media format."""
    actual = format_to_media_type('mp4')
    expected = ('video', 'mp4')

    assert actual == expected
