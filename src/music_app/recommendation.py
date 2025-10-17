"""Recommendation engine for suggesting tracks to play next."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List

from .library import MusicLibrary, Track


class RecommendationEngine:
    """Suggest tracks using hybrid popularity and mood filtering."""

    def __init__(self, library: MusicLibrary) -> None:
        self.library = library

    def recommend_by_mood(self, mood: str, limit: int = 5) -> List[Track]:
        mood_lower = mood.lower()
        matching = [
            track
            for track in self.library.list_tracks()
            if any(mood_lower in entry.lower() for entry in track.moods)
        ]
        return self._rank_by_popularity(matching)[:limit]

    def recommend_similar(self, seed: Track, limit: int = 5) -> List[Track]:
        candidates = [track for track in self.library.list_tracks() if track.id != seed.id]
        ranked = sorted(
            candidates,
            key=lambda track: (
                -self._shared_tags(seed, track),
                track.genre != seed.genre,
                abs((track.bpm or 0) - (seed.bpm or 0)),
            ),
        )
        return ranked[:limit]

    def top_trending(self, limit: int = 10) -> List[Track]:
        return self._rank_by_popularity(self.library.list_tracks())[:limit]

    def _rank_by_popularity(self, tracks: Iterable[Track]) -> List[Track]:
        return sorted(tracks, key=lambda track: (track.play_count, track.last_played or ""), reverse=True)

    @staticmethod
    def _shared_tags(a: Track, b: Track) -> int:
        a_tags = Counter([a.genre, *a.moods])
        b_tags = Counter([b.genre, *b.moods])
        return sum((a_tags & b_tags).values())


__all__ = ["RecommendationEngine"]
