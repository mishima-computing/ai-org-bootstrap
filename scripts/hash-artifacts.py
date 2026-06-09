#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


items = []
for raw in sys.argv[1:]:
    path = Path(raw)
    if path.is_file():
        items.append({"path": str(path), "sha256": sha256(path)})

print(json.dumps({"artifacts": items}, indent=2, ensure_ascii=False))
