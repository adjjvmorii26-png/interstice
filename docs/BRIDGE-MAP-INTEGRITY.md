# Bridge Map Integrity

A deterministic read-only gate for the generated Interstice bridge map.

Run:

```bash
python3 scripts/bridge_map_integrity.py
```

The checker validates the map identity, bridge schema, resonance bounds,
descending ordering, and generated statistics. It never rewrites the map
and fails closed when an invariant is violated.
