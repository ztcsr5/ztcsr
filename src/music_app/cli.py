"""Command line interface for the advanced music software."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .library import MusicLibrary, Track
from .player import MusicPlayer
from .playlist import Playlist
from .recommendation import RecommendationEngine


def _parse_track_payload(payload: str) -> Track:
    data = json.loads(payload)
    return Track(
        id=data["id"],
        title=data["title"],
        artist=data.get("artist", "Unknown"),
        album=data.get("album", "Unknown"),
        duration_seconds=int(data.get("duration_seconds", 0)),
        genre=data.get("genre", "Unknown"),
        moods=data.get("moods", []),
        bpm=data.get("bpm"),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Advanced command-line music application")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("import", help="Import tracks from a JSON file")
    add_parser.add_argument("path", type=Path, help="Path to JSON file containing track data")

    list_parser = subparsers.add_parser("list", help="List tracks in the library")
    list_parser.add_argument("--filter", help="Search query to filter tracks")

    play_parser = subparsers.add_parser("play", help="Simulate playing tracks from a playlist")
    play_parser.add_argument("playlist", type=Path, help="Path to playlist JSON file")

    recommend_parser = subparsers.add_parser("recommend", help="Generate recommendations")
    recommend_parser.add_argument("mode", choices=["mood", "trending"], help="Recommendation mode")
    recommend_parser.add_argument("value", nargs="?", help="Value to use for the recommendation mode")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    library = MusicLibrary()
    player = MusicPlayer(library)
    engine = RecommendationEngine(library)

    if args.command == "import":
        with args.path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
        tracks = [_parse_track_payload(json.dumps(entry)) for entry in payload]
        library.import_tracks(tracks, overwrite=True)
        print(f"Imported {len(tracks)} tracks into the library")
        return 0

    if args.command == "list":
        tracks = library.search(args.filter) if args.filter else library.list_tracks()
        for track in tracks:
            print(f"{track.id}: {track.title} — {track.artist} ({track.genre})")
        return 0

    if args.command == "play":
        with args.playlist.open("r", encoding="utf-8") as fh:
            entries = json.load(fh)
        playlist = Playlist(name=args.playlist.stem, track_ids=entries)
        player.play_playlist(playlist)
        for event in player.history:
            print(f"{event.timestamp.isoformat()} :: {event.action} :: {event.track_id or ''} :: {event.metadata or ''}")
        return 0

    if args.command == "recommend":
        if args.mode == "mood":
            if not args.value:
                parser.error("mood mode requires a value")
            results = engine.recommend_by_mood(args.value)
        else:
            results = engine.top_trending()
        for track in results:
            print(f"{track.id}: {track.title} — {track.artist} [{track.play_count} plays]")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
