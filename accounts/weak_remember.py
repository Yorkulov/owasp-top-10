"""
=== INTENTIONAL VULNERABILITY: A04:2025 - Cryptographic Failures ===
See instructor_solutions/A04-CRYPTO.md

The "remember me" token below is base64(username:expiry_timestamp) with NO
signature/MAC. Any client can forge a token for any username (e.g. the
seeded admin account) and the middleware will trust it blindly. A real
implementation must use django.core.signing (HMAC-signed, tamper-evident)
instead of raw base64.
"""

import base64
import time

COOKIE_NAME = "remember_token"
MAX_AGE_SECONDS = 60 * 60 * 24 * 14


def make_token(username: str) -> str:
    expiry = int(time.time()) + MAX_AGE_SECONDS
    raw = f"{username}:{expiry}"
    return base64.b64encode(raw.encode()).decode()


def parse_token(token: str):
    try:
        raw = base64.b64decode(token.encode()).decode()
        username, expiry = raw.split(":", 1)
        expiry = int(expiry)
    except Exception:
        return None
    if expiry < int(time.time()):
        return None
    return username
