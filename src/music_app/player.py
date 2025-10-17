"""Music player simulation with scheduling and effects."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Deque, Iterable, Optional

from .audio_effects import EqualizerBank, EqualizerPreset
from .library import MusicLibrary, Track
from .playlist import Playlist


@dataclass
class PlaybackEvent:
    """Represents a simulated playback state change."""

    timestamp: datetime
    action: str
    track_id: Optional[str] = None
    metadata: Optional[dict[str, object]] = None


class MusicPlayer:
    """Advanced simulation of a music player with queue management."""

    def __init__(
        self,
        library: MusicLibrary,
        equalizer_bank: Optional[EqualizerBank] = None,
        crossfade_seconds: int = 5,
    ) -> None:
        self.library = library
        self.crossfade_seconds = crossfade_seconds
        self.equalizer_bank = equalizer_bank or EqualizerBank(
            [
                EqualizerPreset("flat"),
                EqualizerPreset("bass_boost", {"bass": 4.0, "low_mid": 2.0}),
                EqualizerPreset("acoustic", {"mid": 2.5, "presence": 3.0, "brilliance": 2.0}),
            ]
        )
        self.current_track: Optional[Track] = None
        self.queue: Deque[str] = deque()
        self.history: Deque[PlaybackEvent] = deque(maxlen=100)
        self.active_preset = "flat"
        self._time_pointer = datetime.utcnow()

    # -- Queue operations -------------------------------------------------
    def enqueue(self, track_ids: Iterable[str]) -> None:
        self.queue.extend(track_ids)

    def play_next(self) -> Optional[Track]:
        if not self.queue:
            self._log_event("queue_empty")
            self.current_track = None
            return None
        track_id = self.queue.popleft()
        track = self.library.get_track(track_id)
        track.mark_played()
        self.current_track = track
        self._advance_time(track.duration_seconds)
        self._log_event("play", track_id)
        return track

    def play_playlist(self, playlist: Playlist) -> None:
        self.enqueue(playlist.track_ids)
        while self.queue:
            self.play_next()
            self._apply_crossfade()

    def skip(self) -> None:
        if self.current_track:
            self._log_event("skip", self.current_track.id)
        self.play_next()

    def rewind(self) -> None:
        if not self.history:
            return
        last_event = self.history.pop()
        if last_event.track_id:
            self.queue.appendleft(last_event.track_id)
            self._log_event("rewind", last_event.track_id)

    # -- Equalizer --------------------------------------------------------
    def set_equalizer_preset(self, preset_name: str) -> EqualizerPreset:
        preset = self.equalizer_bank.get(preset_name)
        self.active_preset = preset.name
        self._log_event("eq_change", metadata={"preset": preset.name})
        return preset

    def transition_equalizer(self, target_preset: str, steps: int = 5) -> None:
        for intermediate in self.equalizer_bank.transition(self.active_preset, target_preset, steps):
            self.active_preset = intermediate.name
            self._log_event("eq_transition", metadata={"preset": intermediate.name})

    # -- Helpers ----------------------------------------------------------
    def _apply_crossfade(self) -> None:
        if self.current_track is None or not self.queue:
            return
        overlap = min(self.crossfade_seconds, self.current_track.duration_seconds)
        self._advance_time(-overlap)
        self._log_event("crossfade", metadata={"seconds": overlap})

    def _log_event(self, action: str, track_id: Optional[str] = None, metadata: Optional[dict[str, object]] = None) -> None:
        event = PlaybackEvent(
            timestamp=self._time_pointer,
            action=action,
            track_id=track_id,
            metadata=metadata,
        )
        self.history.append(event)

    def _advance_time(self, seconds: int) -> None:
        self._time_pointer += timedelta(seconds=seconds)


__all__ = ["MusicPlayer", "PlaybackEvent"]
