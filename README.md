# The Interstice

A bridge cartographer for the whole organism.

The Interstice maps every repo in the `adjjvmorii26-png` constellation
against every living organ in IXpansion, computes *latent resonance*
between repo themes and organ kinships, and surfaces **untouched
bridges** — pairings that share real kinship but have never been
connected. It answers the question: *what should we build next?*

## How it works

1. **Discover** — 37+ constellation repos (themes from descriptions)
   and 286+ living organs (name tokens + declared layers + resonates_with).
2. **Resonate** — fuzzy theme-overlap scoring, normalized by depth.
3. **Bridge** — strongest untouched repo↔organ kinships surfaced.

## Run

```bash
python3 interstice.py          # regenerate data/bridge_map.json
python3 -m pytest tests/       # run tests
```

Open `dashboard/index.html` in a browser for the interactive bridge map.

## Sample untouched bridges (v1.0.0)

| Resonance | Repo                | Organ                 | Layer            |
|-----------|---------------------|-----------------------|------------------|
| 0.23      | glitch-cathedral    | glitch_patterns       | chaos engineering|
| 0.23      | quantum-folio       | quantum_entanglement  | quantum          |
| 0.21      | nebula-archive      | memory_palace         | memory architecture|
| 0.19      | neuroglyph-forge    | dream_archaeologist   | memory archaeology|

## Structure

```
interstice.py          engine: discovery, resonance, bridge-finding
data/bridge_map.json   generated map
dashboard/index.html   standalone interactive viewer (self-contained)
tests/                 unittest suite
```

Pure Python standard library — no dependencies.
