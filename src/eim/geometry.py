"""Geometry helpers for the EIM cosmological collider toy model.

The module is deliberately small and auditable. It builds the dodecahedral
substrate, fixes one orientation per edge, constructs the vertex-edge boundary
operator d1, enumerates the twelve pentagonal faces, and constructs the
edge-face boundary operator d2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict