from __future__ import annotations

from pathlib import Path

from music_app.library import MusicLibrary, Track
from music_app.player import MusicPlayer
from music_app.playlist import Playlist


def test_play_playlist_records_history(tmp_path: Path) -> None:
    library = MusicLibrary(storage_path=tmp_path / "library.json")
    library.import_tracks(
        [
            Track(id="1", title="A", artist="A", album="", duration_seconds=120, genre="Ambient"),
            Track(id="2", title="B", artist="B", album="", duration_seconds=100, genre="Rock"),
        ]
    )

    player = MusicPlayer(library)
    playlist = Playlist(name="test", track_ids=["1", "2"])
    player.play_playlist(playlist)

    actions = [event.action for event in player.history]
    assert "play" in actions
    assert "crossfade" in actions


def test_equalizer_transition(tmp_path: Path) -> None:
    library = MusicLibrary(storage_path=tmp_path / "library.json")
    track = Track(id="1", title="A", artist="A", album="", duration_seconds=120, genre="Ambient")
    library.add_track(track)

    player = MusicPlayer(library)
    player.enqueue([track.id])
    player.play_next()
    player.transition_equalizer("bass_boost", steps=3)

    assert any(event.action == "eq_transition" for event in player.history)
