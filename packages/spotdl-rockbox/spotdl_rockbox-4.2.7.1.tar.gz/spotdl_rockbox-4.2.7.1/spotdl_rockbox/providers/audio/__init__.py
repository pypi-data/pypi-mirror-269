"""
Audio providers for spotdl.
"""

from spotdl_rockbox.providers.audio.bandcamp import BandCamp
from spotdl_rockbox.providers.audio.base import (
    ISRC_REGEX,
    AudioProvider,
    AudioProviderError,
    YTDLLogger,
)
from spotdl_rockbox.providers.audio.piped import Piped
from spotdl_rockbox.providers.audio.sliderkz import SliderKZ
from spotdl_rockbox.providers.audio.soundcloud import SoundCloud
from spotdl_rockbox.providers.audio.youtube import YouTube
from spotdl_rockbox.providers.audio.ytmusic import YouTubeMusic

__all__ = [
    "YouTube",
    "YouTubeMusic",
    "SliderKZ",
    "SoundCloud",
    "BandCamp",
    "Piped",
    "AudioProvider",
    "AudioProviderError",
    "YTDLLogger",
    "ISRC_REGEX",
]
