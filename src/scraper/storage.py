"""
Persistent storage for seen listing IDs.
Uses a simple JSON file so we only alert on genuinely new listings.
"""
import json
import os
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent.parent.parent / "data" / "seen_listings.json"


def _load(path: Path) -> set[str]:
    if path.exists():
        with open(path) as f:
            data = json.load(f)
        return set(data.get("seen", []))
    return set()


def _save(seen: set[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump({"seen": sorted(seen)}, f, indent=2)


def filter_new(listings: list[dict], path: Path = DEFAULT_PATH) -> list[dict]:
    """Return only listings not seen before, and persist their IDs."""
    seen = _load(path)
    new = [l for l in listings if l["id"] not in seen]
    if new:
        seen.update(l["id"] for l in new)
        _save(seen, path)
    return new


def mark_seen(listing_ids: list[str], path: Path = DEFAULT_PATH) -> None:
    seen = _load(path)
    seen.update(listing_ids)
    _save(seen, path)


def reset(path: Path = DEFAULT_PATH) -> None:
    """Clear all seen listings (re-run from scratch)."""
    _save(set(), path)
