#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone

payload = {
    "status": "not_configured",
    "note": "audit bundle builder is not implemented yet",
    "created_at": datetime.now(timezone.utc).isoformat(),
}

print(json.dumps(payload, indent=2, ensure_ascii=False))
