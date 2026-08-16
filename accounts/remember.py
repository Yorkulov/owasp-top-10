"""
"Remember me" token helpers used by the login flow and its auto-login
middleware. See accounts/middleware.py for where these are consumed.
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
