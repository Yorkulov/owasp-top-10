"""
A tiny "internal-only" service used for the A01 SSRF scenario. In a real
deployment this would be a private microservice unreachable from the
public internet (e.g. an internal metadata/API host). Here, since
everything runs on localhost for a single student, it is instead gated by
a shared internal-only header that only server-side code (the seller
panel's "import image from URL" feature - see sellerpanel/views.py) is
supposed to send. A normal browser request never sends this header.
"""

INTERNAL_HEADER = "X-Internal-Request"
INTERNAL_HEADER_VALUE = "vega-internal-svc-2025"
