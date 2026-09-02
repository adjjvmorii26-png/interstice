"""The Interstice — unit tests for bridge cartography."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from interstice import (
    Repo, Organ,
    discover_organs,
    resonance,
    find_bridges,
    build_map,
    _fuzzy_overlap,
)


def test_resonance_exact_match():
    repo = Repo(name="quietus-array", themes={"silence": 0.9, "rest": 0.5})
    organ = Organ(name="silence_orchard", layer="stillness", themes={"silence": 0.7, "rest": 0.4})
    assert resonance(repo, organ) > resonance(repo, Organ(name="x", themes={"unrelated": 0.9}))


def test_resonance_zero_when_no_themes():
    r = Repo(name="a")
    o = Organ(name="b")
    assert resonance(r, o) == 0.0


def test_fuzzy_overlap_substring():
    score = _fuzzy_overlap({"branch": 0.7}, {"branching": 0.6})
    assert score > 0
    assert score < 0.7 * 0.6  # substring match is discounted


def test_discover_organs_finds_living_triad():
    organs = discover_organs()
    assert len(organs) > 100
    assert all(o.name for o in organs)
    assert any(o.layer != "unknown" for o in organs)


def test_build_map_shape():
    m = build_map()
    assert m["name"] == "The Interstice"
    assert m["statistics"]["repos"] >= 30
    assert m["statistics"]["organs"] >= 100
    assert m["statistics"]["untouched_bridges"] > 0
    assert all("repo" in b and "organ" in b and "resonance" in b for b in m["top_bridges"])


def test_bridges_sorted_desc():
    m = build_map()
    rs = [b["resonance"] for b in m["top_bridges"]]
    assert rs == sorted(rs, reverse=True)


def test_no_duplicate_organ_overload():
    m = build_map()
    # at most 5 organ entries in top bridges (per engine top_k)
    from collections import Counter
    c = Counter(b["organ"] for b in m["top_bridges"])
    assert max(c.values()) <= 5


def test_generated_map_file_matches_engine():
    data = json.loads((ROOT / "data" / "bridge_map.json").read_text())
    assert data["statistics"]["untouched_bridges"] > 0
    assert data["statistics"] == build_map()["statistics"]
