"""Audio effect modeling utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable


FREQUENCY_BANDS = ("sub", "bass", "low_mid", "mid", "high_mid", "presence", "brilliance")


@dataclass
class EqualizerPreset:
    """Represents equalizer gains for fixed frequency bands."""

    name: str
    gains: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for band in FREQUENCY_BANDS:
            self.gains.setdefault(band, 0.0)

    def blend(self, other: "EqualizerPreset", ratio: float) -> "EqualizerPreset":
        """Return a new preset interpolated between this preset and another."""

        ratio = max(0.0, min(1.0, ratio))
        blended = {
            band: self.gains[band] * (1 - ratio) + other.gains[band] * ratio
            for band in FREQUENCY_BANDS
        }
        return EqualizerPreset(name=f"blend({self.name},{other.name})", gains=blended)


class EqualizerBank:
    """Collection of EQ presets with utilities for transitions."""

    def __init__(self, presets: Iterable[EqualizerPreset] | None = None) -> None:
        self._presets: Dict[str, EqualizerPreset] = {}
        if presets:
            for preset in presets:
                self.add_preset(preset)

    def add_preset(self, preset: EqualizerPreset) -> None:
        self._presets[preset.name] = preset

    def get(self, name: str) -> EqualizerPreset:
        try:
            return self._presets[name]
        except KeyError as exc:
            raise KeyError(f"Equalizer preset {name!r} not found") from exc

    def transition(self, from_preset: str, to_preset: str, steps: int) -> Iterable[EqualizerPreset]:
        start = self.get(from_preset)
        end = self.get(to_preset)
        if steps <= 1:
            yield end
            return
        for index in range(1, steps + 1):
            yield start.blend(end, index / steps)


__all__ = ["EqualizerPreset", "EqualizerBank", "FREQUENCY_BANDS"]
