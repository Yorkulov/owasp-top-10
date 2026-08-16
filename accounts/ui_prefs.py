"""
=== INTENTIONAL VULNERABILITY: A08:2025 - Software or Data Integrity Failures ===
See instructor_solutions/A08-INTEGRITY.md

The ui_prefs cookie stores client-side "preferences" as base64(JSON) with no
signature. It is meant only for theme/layout preferences, but the beta
tools page mistakenly trusts a "role" field inside it for an authorization
decision. A real implementation must never use unsigned client state for
access control - use django.core.signing or re-check the role server-side
from the database.
"""

import base64
import json

COOKIE_NAME = "ui_prefs"


def default_prefs(role: str) -> dict:
    return {"theme": "dark", "density": "comfortable", "role": role}


def encode_prefs(prefs: dict) -> str:
    return base64.b64encode(json.dumps(prefs).encode()).decode()


def decode_prefs(raw: str):
    try:
        return json.loads(base64.b64decode(raw.encode()).decode())
    except Exception:
        return None
