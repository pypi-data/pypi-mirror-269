"""
Lyrics providers for spotdl.
"""

from spotdl_rockbox.providers.lyrics.azlyrics import AzLyrics
from spotdl_rockbox.providers.lyrics.base import LyricsProvider
from spotdl_rockbox.providers.lyrics.genius import Genius
from spotdl_rockbox.providers.lyrics.musixmatch import MusixMatch
from spotdl_rockbox.providers.lyrics.synced import Synced

__all__ = ["AzLyrics", "Genius", "MusixMatch", "Synced", "LyricsProvider"]
