from __future__ import annotations

from pathlib import Path

from music_app.library import MusicLibrary, Track
from music_app.recommendation import RecommendationEngine


def _seed_library(library: MusicLibrary) -> None:
    library.import_tracks(
        [
            Track(id="1", title="A", artist="A", album="", duration_seconds=100, genre="Ambient", moods=["calm"], bpm=90, play_count=10),
            Track(id="2", title="B", artist="B", album="", duration_seconds=100, genre="Ambient", moods=["calm", "focus"], bpm=92, play_count=5),
            Track(id="3", title="C", artist="C", album="", duration_seconds=100, genre="Rock", moods=["energetic"], bpm=120, play_count=20),
        ],
        overwrite=True,
    )


def test_recommend_by_mood(tmp_path: Path) -> None:
    library = MusicLibrary(storage_path=tmp_path / "library.json")
    _seed_library(library)
    engine = RecommendationEngine(library)

    results = engine.recommend_by_mood("calm")
    assert [track.id for track in results] == ["1", "2"]


def test_recommend_similar(tmp_path: Path) -> None:
    library = MusicLibrary(storage_path=tmp_path / "library.json")
    _seed_library(library)
    engine = RecommendationEngine(library)

    seed = library.get_track("1")
    results = engine.recommend_similar(seed)
    assert results[0].id == "2"
