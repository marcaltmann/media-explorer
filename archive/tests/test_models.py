from django.test import TestCase

from archive.models import MediaFile


def video():
    return MediaFile(media_type="video/mp4")


def audio():
    return MediaFile(media_type="audio/mp3")


class ResourceModelTests(TestCase):
    def test_is_video_with_video(self):
        """is_video() returns True for videos."""
        self.assertIs(video().is_video(), True)

    def test_is_video_with_other(self):
        """is_video() returns False for non-videos."""
        self.assertIs(audio().is_video(), False)

    def test_is_audio_with_audio(self):
        """is_audio() returns True for audios."""
        self.assertIs(audio().is_audio(), True)

    def test_is_audio_with_other(self):
        """is_audio() returns False for non-audios."""
        self.assertIs(video().is_audio(), False)
