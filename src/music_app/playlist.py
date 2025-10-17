"""Playlist management utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from .library import MusicLibrary, Track


@dataclass
class Playlist:
    """A playlist is an ordered collection of track identifiers."""

    name: str
    track_ids: List[str] = field(default_factory=list)

    def add_track(self, track_id: str) -> None:
        if track_id not in self.track_ids:
            self.track_ids.append(track_id)

    def add_tracks(self, track_ids: Iterable[str]) -> None:
        for track_id in track_ids:
            self.add_track(track_id)

    def remove_track(self, track_id: str) -> None:
        if track_id in self.track_ids:
            self.track_ids.remove(track_id)

    def reorder(self, old_index: int, new_index: int) -> None:
        track_id = self.track_ids.pop(old_index)
        self.track_ids.insert(new_index, track_id)

    def expand(self, library: MusicLibrary) -> List[Track]:
        return [library.get_track(track_id) for track_id in self.track_ids]


class PlaylistCollection:
    """A collection of playlists stored in memory."""

    def __init__(self) -> None:
        self._playlists: dict[str, Playlist] = {}

    def add(self, playlist: Playlist) -> None:
        if playlist.name in self._playlists:
            raise ValueError(f"Playlist {playlist.name!r} already exists")
        self._playlists[playlist.name] = playlist

    def get(self, name: str) -> Playlist:
        try:
            return self._playlists[name]
        except KeyError as exc:
            raise KeyError(f"Playlist {name!r} not found") from exc

    def list(self) -> List[Playlist]:
        return list(self._playlists.values())


__all__ = ["Playlist", "PlaylistCollection"]
