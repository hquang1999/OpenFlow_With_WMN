from __future__ import annotations
from typing import Any, Optional

type NodeId = int
type EdgeId = int

class Edge:
    """Data associated with the edges of the graph"""

    cost: float
    max_flow: float
    def __new__(cls, cost: float, max_flow: float) -> Edge: ...
    def __repr__(self) -> str: ...

class FlowPath:
    """Path through the graph with a cost and flow"""

    cost: float
    flow: float
    edges: list[EdgeId]
    def __new__(cls, cost: float, flow: float, edges: list[EdgeId]) -> FlowPath: ...
    def __repr__(self) -> str: ...

class Graph:
    """
    Python wrapper of Rust Graph type.
    """
    def __new__(cls) -> Graph: ...
    def __repr__(self) -> str: ...
    def add_node(self, weight: Any) -> NodeId:
        """Add node to graph and return its id."""
    def get_node(self, id: NodeId) -> Optional[Any]:
        """Get node with the given node id"""
    def remove_node(self, a: NodeId):
        """Remove node from graph."""
    def add_edge(self, a: NodeId, b: NodeId, weight: Edge) -> EdgeId:
        """Add edge from `a` to `b` to graph with associated data `weight` and return its id."""
    def remove_edge(self, a: EdgeId) -> Optional[Edge]:
        """Remove edge from graph. Return the removed edge's data."""
    def edges_directed(self, a: NodeId, outgoing: bool) -> list[EdgeId]:
        """
        All edges of a, in the specified direction.

        - Outgoing=true: All edges from a.
        - Outgoing=false: All edges to a.
        """
    def ranked_max_flow(self, source: NodeId, goal: NodeId) -> list[FlowPath]:
        """
        Finds multiple `FlowPath`s going from `source` to `goal` sorted from lowest cost to highest cost.
        The combination of these paths is a minimum cost maximum flow from `source` to `goal`
        """
