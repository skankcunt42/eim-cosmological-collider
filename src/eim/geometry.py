"""Dodecahedral geometry helpers for EIM projector audits."""
from dataclasses import dataclass
from typing import Dict, Tuple
import networkx as nx
import numpy as np

Edge = Tuple[int, int]
Face = Tuple[int, ...]

@dataclass(frozen=True)
class DodecahedralGeometry:
    graph: nx.Graph
    vertices: Tuple[int, ...]
    edges: Tuple[Edge, ...]
    edge_index: Dict[Edge, int]
    faces