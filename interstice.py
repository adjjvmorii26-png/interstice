"""The Interstice — bridge cartographer for the whole organism.

Discovers every repo in the adjjvmorii26-png constellation and every
living organ in IXpansion, then computes latent resonance between
repo-themes and organ-kinships to surface UNTOUCHED BRIDGES —
pairings with real kinship that have never been connected.

Pure stdlib. Run:  python3 interstice.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent

# Theme signatures for each known repo family (from descriptions + structure).
REPO_THEMES: Dict[str, Dict[str, float]] = {
    "ixpansion": {"consciousness": 0.9, "evolution": 0.8, "wave": 0.8, "agent": 0.7, "resonance": 0.7, "dream": 0.6, "entropy": 0.6},
    "nexus-observatory": {"observatory": 0.9, "resonance": 0.8, "interop": 0.7, "recursive": 0.6, "paradox": 0.6, "temporal": 0.5},
    "solid-organism": {"organism": 0.9, "pulse": 0.7, "phoenix": 0.6, "fractal": 0.6, "lattice": 0.5},
    "omega-fractal-engine": {"fractal": 0.9, "chaos": 0.7, "nucleus": 0.6, "ritual": 0.6, "archives": 0.5},
    "probability-engine": {"probability": 0.9, "chance": 0.8, "collapse": 0.7, "quantum": 0.6},
    "quietus-array": {"silence": 0.9, "absence": 0.8, "calm": 0.6, "rest": 0.5},
    "multiself-engine": {"identity": 0.9, "branch": 0.7, "self": 0.7, "divergence": 0.6},
    "parallax-engine": {"perspective": 0.9, "depth": 0.7, "veil": 0.6, "distortion": 0.5},
    "attention-labyrinth": {"attention": 0.9, "focus": 0.7, "drift": 0.6, "concentration": 0.5},
    "glitch-cathedral": {"glitch": 0.9, "corruption": 0.7, "repair": 0.6, "noise": 0.6, "chaos": 0.6},
    "phaseshift-manifold": {"phase": 0.8, "matter": 0.7, "plasma": 0.6, "state": 0.5},
    "geometric-anthology": {"geometry": 0.8, "form": 0.7, "tessellation": 0.6, "shape": 0.5},
    "semiotic-engine": {"sign": 0.8, "meaning": 0.7, "glyph": 0.6, "metaphor": 0.6},
    "ontoforge-singularity": {"being": 0.8, "essence": 0.7, "reality": 0.7, "ontology": 0.6},
    "neuroglyph-forge": {"cognition": 0.8, "thought": 0.7, "memory": 0.6, "dream": 0.6, "emotion": 0.5},
    "chronovore-archive": {"time": 0.8, "archive": 0.7, "chrono": 0.7, "memory": 0.6},
    "paraconstruct-engine": {"impossible": 0.8, "architecture": 0.7, "recursive": 0.6, "space": 0.5},
    "hyperfractal-relay": {"fractal": 0.8, "relay": 0.7, "bloom": 0.6, "echo": 0.5},
    "antimemetic-architecton": {"absence": 0.8, "erasure": 0.7, "inversion": 0.6, "negative": 0.5},
    "sensorium-engine": {"sensory": 0.8, "sound": 0.6, "tactile": 0.6, "smell": 0.6, "vision": 0.5},
    "topologic-alchemy": {"knot": 0.8, "warp": 0.7, "manifold": 0.7, "topology": 0.6},
    "quantum-folio": {"quantum": 0.8, "entangle": 0.7, "spin": 0.6, "decoherence": 0.5},
    "lexicon-chrysalis": {"language": 0.8, "linguistic": 0.7, "molt": 0.6, "word": 0.6},
    "luminant-reliquary": {"light": 0.8, "crystal": 0.7, "memory": 0.6, "luminous": 0.5},
    "auric-labyrinth": {"golden": 0.8, "spiral": 0.7, "cantor": 0.6, "sacred": 0.5},
    "polychron-atlas": {"time": 0.8, "cartography": 0.7, "paradox": 0.6, "multi": 0.5},
    "chronocrypt-orrery": {"time": 0.8, "cyclic": 0.7, "gyre": 0.6, "orbit": 0.5},
    "echotide-engine": {"tide": 0.8, "wave": 0.7, "reef": 0.6, "echo": 0.6},
    "nebula-archive": {"memory": 0.8, "foundry": 0.7, "observatory": 0.6, "vault": 0.5},
    "parallax": {"perspective": 0.8, "protocol": 0.7, "relational": 0.6, "mesh": 0.5},
    "metamorph-forge": {"transformation": 0.8, "forge": 0.7, "morph": 0.7, "evolution": 0.5},
    "astral-forge": {"astral": 0.7, "forge": 0.7, "star": 0.6, "cosmic": 0.5},
    "agent-workforce": {"agent": 0.8, "workforce": 0.7, "faction": 0.6, "evolution": 0.5},
    "workforce-": {"agent": 0.8, "workforce": 0.7, "evolution": 0.6, "quest": 0.5},
    "multi-agent": {"agent": 0.8, "multi": 0.7, "swarm": 0.6, "cooperation": 0.5},
    "yaweht": {"agent": 0.7, "federated": 0.6, "token": 0.6, "lattice": 0.5},
    "nextjs-boilerplate": {"web": 0.6, "nextjs": 0.6, "ui": 0.5, "react": 0.5},
}


@dataclass
class Repo:
    name: str
    description: str = ""
    themes: Dict[str, float] = field(default_factory=dict)
    path: str = ""


@dataclass
class Organ:
    name: str
    layer: str = "unknown"
    resonance: float = 0.5
    kin: List[str] = field(default_factory=list)
    themes: Dict[str, float] = field(default_factory=dict)


def discover_repos(repo_dir: Path | None = None) -> List[Repo]:
    """Discover repos from the constellation theme map + optional local paths."""
    repos: List[Repo] = []
    for name, themes in REPO_THEMES.items():
        repos.append(Repo(name=name, description=f"constellation repo: {name}", themes=themes))
    if repo_dir and repo_dir.exists():
        for d in sorted(repo_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                for r in repos:
                    if r.name == d.name:
                        r.path = str(d)
    return repos


def discover_organs(api_dir: Path | None = None) -> List[Organ]:
    """Discover living organs from the IXpansion api/ directory.

    Each organ contributes:
    - name tokens (eternal_flame -> eternal, flame)
    - declared layer phrase
    - declared resonates_with keywords
    """
    organs: List[Organ] = []
    api_dir = api_dir or (ROOT / ".." / "Documents" / "Codex" / "2026-08-22" / "chmod-x-nexus-observatory-nexus-boot" / "api")
    if api_dir and api_dir.exists():
        for f in sorted(api_dir.glob("*.py")):
            if f.stem in ("__init__", "index", "unified_router"):
                continue
            try:
                src = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "def coherence_vitals" not in src or "def handler" not in src:
                continue

            layer = "unknown"
            lm = re.search(r"""["']layer["']\s*:\s*["']([^"']+)["']""", src)
            if lm:
                layer = lm.group(1).strip().lower()
            rm = re.search(r"""["']resonance["']\s*:\s*([0-9.]+)""", src)
            resonance = float(rm.group(1)) if rm else 0.5

            themes: Dict[str, float] = {}
            for tok in re.findall(r"[a-z][a-z0-9]{2,}", f.stem.replace("_", " ")):
                themes[tok] = 0.7
            for tok in re.findall(r"[a-z]{3,}", layer):
                themes[tok] = themes.get(tok, 0.5) + 0.2
            km = re.search(r"def resonates_with\(\) -> list:\s*return \[([^\]]*)\]", src, re.S)
            kin: List[str] = []
            if km:
                kin = re.findall(r'"([a-z_]{3,})"', km.group(1))
                for kw in kin:
                    themes[kw] = max(themes.get(kw, 0), 0.5)

            organs.append(Organ(name=f.stem, layer=layer, resonance=round(resonance, 3),
                                kin=kin, themes={k: round(v, 3) for k, v in themes.items()}))
    return organs


def _fuzzy_overlap(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Theme overlap with substring-level fuzz (branch<->branch counts)."""
    score = 0.0
    for x, xw in a.items():
        for y, yw in b.items():
            if x == y:
                score += xw * yw
            elif x in y or y in x:
                score += xw * yw * 0.5
            elif x.startswith(y[:4]) or y.startswith(x[:4]):
                score += xw * yw * 0.22
    return score


def resonance(repo: Repo, organ: Organ) -> float:
    if not repo.themes or not organ.themes:
        return 0.0
    score = _fuzzy_overlap(repo.themes, organ.themes)
    depth = math.sqrt(len(repo.themes) * len(organ.themes)) or 1.0
    return round(min(1.0, score / depth), 4)


def find_bridges(repos: List[Repo], organs: List[Organ], top_k: int = 5) -> List[Dict[str, Any]]:
    """Surface the strongest latent repo<->organ kinships."""
    pairs = []
    for repo in repos:
        for organ in organs:
            score = resonance(repo, organ)
            if score > 0:
                pairs.append({
                    "repo": repo.name,
                    "organ": organ.name,
                    "organ_layer": organ.layer,
                    "resonance": score,
                    "untouched": True,
                })
    pairs.sort(key=lambda b: b["resonance"], reverse=True)

    bridges: List[Dict[str, Any]] = []
    seen: set = set()
    for b in pairs:
        if b["organ"] in seen:
            if b["resonance"] < 0.28:
                continue
        if sum(1 for x in bridges if x["repo"] == b["repo"]) > top_k:
            continue
        seen.add(b["organ"])
        bridges.append(b)
        if len(bridges) >= 75:
            break
    return bridges


def build_map(repo_dir: Path | None = None, api_dir: Path | None = None) -> Dict[str, Any]:
    repos = discover_repos(repo_dir)
    organs = discover_organs(api_dir)
    bridges = find_bridges(repos, organs)

    by_repo: Dict[str, List[Dict[str, Any]]] = {}
    for b in bridges:
        by_repo.setdefault(b["repo"], []).append(b)

    return {
        "name": "The Interstice",
        "version": "1.0.0",
        "repos": [{"name": r.name, "description": r.description, "themes": sorted(r.themes.keys())} for r in repos],
        "organs": [{"name": o.name, "layer": o.layer, "resonance": o.resonance} for o in organs],
        "bridge_count": len(bridges),
        "top_bridges": bridges,
        "statistics": {
            "repos": len(repos),
            "organs": len(organs),
            "untouched_bridges": len(bridges),
            "unique_repos_with_bridges": len(by_repo),
            "known_layer_organs": sum(1 for o in organs if o.layer != "unknown"),
        },
    }


def main() -> int:
    map_data = build_map()
    out = ROOT / "data" / "bridge_map.json"
    out.write_text(json.dumps(map_data, indent=2))
    print(f"[interstice] wrote {out}")
    s = map_data["statistics"]
    print(f"  repos: {s['repos']} | organs: {s['organs']} | untouched bridges: {s['untouched_bridges']}")
    print(f"  known-layer organs: {s['known_layer_organs']}")
    print("  top 10 untouched bridges:")
    for b in map_data["top_bridges"][:10]:
        print(f"    {b['resonance']:.2f}  {b['repo']:<28} <-> {b['organ']:<30} ({b['organ_layer']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
