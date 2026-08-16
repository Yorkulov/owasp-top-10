"""Client-side UI preferences (theme, layout density) stored in a cookie."""

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
