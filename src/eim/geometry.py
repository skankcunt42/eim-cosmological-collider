"""Geometry helpers for the EIM cosmological collider toy model.

This module keeps the geometric layer small and auditable.  We use
NetworkX's dodecahedral graph, orient each edge once, construct the
vertex-edge boundary operator d1, and enumerate the 12 pentagonal faces used
for the face-boundary operator d2.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import networkx as nx
import numpy as np

Edge = Tuple[int, int