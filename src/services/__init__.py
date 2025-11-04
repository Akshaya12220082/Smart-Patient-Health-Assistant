"""
Service clients: maps and notifications.
"""

from .maps import find_hospitals_nearby
from .notify import send_sos

__all__ = [
    "find_hospitals_nearby",
    "send_sos",
]


