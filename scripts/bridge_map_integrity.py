"""Validate the generated Interstice bridge map without mutating it."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "bridge_map.json"

def validate(data: dict) -> list[str]:
    errors = []
    if data.get("name") != "The Interstice":
        errors.append("invalid map name")
    bridges = data.get("top_bridges", [])
    if data.get("bridge_count") != len(bridges):
        errors.append("bridge_count mismatch")
    if any(not {"repo", "organ", "resonance", "untouched"} <= set(b) for b in bridges):
        errors.append("bridge schema violation")
    scores = [b["resonance"] for b in bridges]
    if scores != sorted(scores, reverse=True):
        errors.append("bridges are not sorted by resonance")
    if any(not (0 <= b["resonance"] <= 1) for b in bridges):
        errors.append("resonance outside [0,1]")
    stats = data.get("statistics", {})
    if stats.get("untouched_bridges") != len(bridges):
        errors.append("statistics mismatch")
    return errors

def main() -> int:
    data = json.loads(MAP.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1
    print(json.dumps({
        "status": "PASS",
        "bridges": len(data["top_bridges"]),
        "repos": data["statistics"].get("repos"),
        "organs": data["statistics"].get("organs")
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
