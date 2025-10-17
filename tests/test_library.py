from __future__ import annotations

from pathlib import Path

from music_app.library import MusicLibrary, Track


def test_add_and_retrieve_track(tmp_path: Path) -> None:
    storage = tmp_path / "library.json"
    library = MusicLibrary(storage_path=storage)
    track = Track(
        id="001",
        title="Test",
        artist="Artist",
        album="Album",
        duration_seconds=200,
        genre="Genre",
    )
    library.add_track(track)

    retrieved = library.get_track("001")
    assert retrieved.title == "Test"
    assert retrieved.play_count == 0


def test_search_tracks(tmp_path: Path) -> None:
    storage = tmp_path / "library.json"
    library = MusicLibrary(storage_path=storage)
    library.import_tracks(
        [
            Track(id="1", title="Calm Sea", artist="A", album="", duration_seconds=100, genre="Ambient", moods=["calm"]),
            Track(id="2", title="Storm", artist="B", album="", duration_seconds=100, genre="Rock", moods=["energetic"]),
        ]
    )

    results = library.search("calm")
    assert [track.id for track in results] == ["1"]
