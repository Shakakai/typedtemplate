"""The `version` module holds the version information for TypedTemplate."""
from __future__ import annotations as _annotations

__all__ = 'VERSION', 'version_short'

VERSION = '0.2.1'
"""The version of TypedTemplate."""


def version_short() -> str:
    """Return the `major.minor` part of TypedTemplate version.

    It returns '2.1' if TypedTemplate version is '2.1.1'.
    """
    return '.'.join(VERSION.split('.')[:2])
