from __future__ import annotations
from typing import Optional
class Edge:
    """
    Data associated with the edges of the graph
    """
    cost: float
    max_flow: float
    def __new__(cls, cost: float, max_flow: float) -> Edge: ...
    def __repr__(self) -> str: ...
class FlowPath:
    """
    Path through the graph with a cost and flow
    """
    cost: float
    flow: float
    edges: list[int]
    def __new__(cls, cost: float, flow: float, edges: list[int]) -> FlowPath: ...
    def __repr__(self) -> str: ...
class Graph:
    """
    Python wrapper of Rust Graph type.
    """
    def __new__(cls) -> Graph: ...
    def __repr__(self) -> str: ...
    def add_node(self) -> int:
        """
        Add node to graph and return its id.
        """
    def add_edge(self, a: int, b: int, weight: Edge) -> int:
        """
        Add edge from `a` to `b` to graph with associated data `weight` and return its id.
        """
    def remove_node(self, a: int):
        """
        Remove node from graph.
        """
    def remove_edge(self, a: int) -> Optional[Edge]:
        """
        Remove edge from graph. Return the removed edge's data.
        """
    def ranked_max_flow(self, source: int, goal: int) -> list[FlowPath]:
        """
        Finds multiple `FlowPath`s going from `source` to `goal` sorted from lowest cost to highest cost.
        The combination of these paths is a minimum cost maximum flow from `source` to `goal`
        """
