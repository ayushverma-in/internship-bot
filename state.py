"""
Tracks which listings have already been sent so we never repeat one.
The state file gets committed back to the repo by the GitHub Action
after every run (see .github/workflows/daily_internships.yml).
"""
import json
import hashlib
import os
from datetime import datetime, timedelta, timezone

from config import STATE_RETENTION_DAYS

STATE_PATH = os.path.join(os.path.dirname(__file__), "seen_listings.json")


def listing_id(listing: dict) -> str:
    """Stable hash for a listing so the same posting isn't sent twice
    even if different sources phrase the title slightly differently."""
    raw = f"{listing.get('company','').lower().strip()}|{listing.get('title','').lower().strip()}|{listing.get('link','').strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_state(state: dict) -> None:
    # purge anything older than the retention window so this file
    # doesn't grow forever
    cutoff = datetime.now(timezone.utc) - timedelta(days=STATE_RETENTION_DAYS)
    pruned = {
        k: v for k, v in state.items()
        if datetime.fromisoformat(v) > cutoff
    }
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(pruned, f, indent=2)


def mark_seen(state: dict, lid: str) -> None:
    state[lid] = datetime.now(timezone.utc).isoformat()


def already_seen(state: dict, lid: str) -> bool:
    return lid in state
