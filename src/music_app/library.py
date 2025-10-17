"""Tools for managing the music library and metadata persistence."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

DEFAULT_STORAGE_PATH = Path(os.environ.get("ZTSCR_LIBRARY_PATH", Path.home() / ".ztcsr_music" / "library.json"))


def _ensure_storage_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class Track:
    """Representation of a single track in the library."""

    id: str
    title: str
    artist: str
    album: str
    duration_seconds: int
    genre: str
    moods: List[str] = field(default_factory=list)
    bpm: Optional[int] = None
    last_played: Optional[str] = None
    play_count: int = 0

    def mark_played(self) -> None:
        """Increment play count and update last played timestamp."""

        self.play_count += 1
        self.last_played = datetime.utcnow().isoformat()


class MusicLibrary:
    """Persistent store for tracks and associated metadata."""

    def __init__(self, storage_path: Path = DEFAULT_STORAGE_PATH) -> None:
        self.storage_path = storage_path
        _ensure_storage_directory(self.storage_path)
        self._tracks: Dict[str, Track] = {}
        self._load()

    # -- Persistence -----------------------------------------------------
    def _load(self) -> None:
        if not self.storage_path.exists():
            self._tracks = {}
            return
        with self.storage_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._tracks = {track_id: Track(**payload) for track_id, payload in data.items()}

    def save(self) -> None:
        _ensure_storage_directory(self.storage_path)
        payload = {track_id: asdict(track) for track_id, track in self._tracks.items()}
        with self.storage_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

    # -- Library operations ----------------------------------------------
    def add_track(self, track: Track, overwrite: bool = False) -> None:
        if not overwrite and track.id in self._tracks:
            raise ValueError(f"Track with id {track.id!r} already exists")
        self._tracks[track.id] = track
        self.save()

    def remove_track(self, track_id: str) -> None:
        if track_id not in self._tracks:
            raise KeyError(f"Track with id {track_id!r} does not exist")
        del self._tracks[track_id]
        self.save()

    def get_track(self, track_id: str) -> Track:
        try:
            return self._tracks[track_id]
        except KeyError as exc:
            raise KeyError(f"Track with id {track_id!r} not found") from exc

    def list_tracks(self) -> List[Track]:
        return list(self._tracks.values())

    def search(self, query: str) -> List[Track]:
        query_lower = query.lower()
        return [
            track
            for track in self._tracks.values()
            if query_lower in track.title.lower()
            or query_lower in track.artist.lower()
            or query_lower in track.album.lower()
            or query_lower in track.genre.lower()
            or any(query_lower in mood.lower() for mood in track.moods)
        ]

    def import_tracks(self, tracks: Iterable[Track], overwrite: bool = False) -> None:
        for track in tracks:
            self.add_track(track, overwrite=overwrite)

    def update_track_metadata(self, track_id: str, **metadata: object) -> Track:
        track = self.get_track(track_id)
        for key, value in metadata.items():
            if not hasattr(track, key):
                raise AttributeError(f"Track has no attribute {key!r}")
            setattr(track, key, value)
        self.save()
        return track

    def top_tracks(self, limit: int = 10) -> List[Track]:
        return sorted(self._tracks.values(), key=lambda t: t.play_count, reverse=True)[:limit]

    def recently_played(self, limit: int = 10) -> List[Track]:
        return sorted(
            (track for track in self._tracks.values() if track.last_played),
            key=lambda t: t.last_played or "",
            reverse=True,
        )[:limit]


__all__ = ["MusicLibrary", "Track", "DEFAULT_STORAGE_PATH"]
