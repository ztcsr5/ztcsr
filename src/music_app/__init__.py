"""Advanced music software package."""

from .library import MusicLibrary, Track
from .player import MusicPlayer
from .playlist import Playlist
from .recommendation import RecommendationEngine

__all__ = [
    "MusicLibrary",
    "Track",
    "MusicPlayer",
    "Playlist",
    "RecommendationEngine",
]
