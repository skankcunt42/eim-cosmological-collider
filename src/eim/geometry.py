"""Dodecahedral graph helpers."""
from dataclasses import dataclass
import networkx as nx
import numpy as np

@dataclass(frozen=True)
class DodecahedralGeometry:
    graph: object
    vertices: tuple
    edges: tuple
    d1: object

def build_dodecahedral_geometry():
    g = nx.dodecahedral_graph()
    vertices = tuple(sorted(g.nodes()))
    edges = tuple(sorted((min(a,b), max(a,b)) for a,b in g.edges()))
    vi = {v:i for i,v in enumerate(vertices)}
    d