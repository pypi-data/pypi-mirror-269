"""Simple and complex data types for the graph module."""

import bisect
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Annotated, Literal, TypeVar

import numpy as np
import numpy.typing as npt


NDType = TypeVar("NDType", bound=np.generic)
Vector = Annotated[npt.NDArray[NDType], Literal["N", 1]]

type NodeSequence = Sequence[Node]
type EdgeSequence = Sequence[Edge]
type EdgeDefinitionSequence = Sequence[tuple[int | float, tuple[tuple, tuple]]]
type AdjacencyMap = Mapping[Node, Sequence[Edge]]
type HeuristicDistanceCallable = Callable[[Node, Node], int | float]
type ValidEdgeCallable = Callable[[Edge], bool]
type EdgeWeightCallable = Callable[Graph, Edge]


@dataclass
class Node:
    """A node in a graph."""
    coordinates: Vector[np.float64]
    properties: dict = field(default_factory=dict)

    def __post_init__(self):
        self.coordinates = np.array(self.coordinates, dtype=np.float64)
        if not isinstance(self.properties, dict):
            self.properties = dict(self.properties)

    def __hash__(self):
        return hash(self.coordinates.tobytes()) # May not work for mixed array shapes; intended for Vectors only.

    def __eq__(self, other):
        return np.all(self.coordinates == other.coordinates)

    def __lt__(self, other: 'Node') -> bool:
        return not np.all(self.coordinates < other.coordinates)

    def __add__(self, other):
        if isinstance(other, Node):
            other = other.coordinates
        return Node(self.coordinates + other)

    def __sub__(self, other):
        if isinstance(other, Node):
            other = other.coordinates
        return Node(self.coordinates - other)

    def __mul__(self, other):
        if isinstance(other, Node):
            other = other.coordinates
        return Node(self.coordinates * other)

    def __truediv__(self, other):
        if isinstance(other, Node):
            other = other.coordinates
        return Node(self.coordinates / other)

    def __floordiv__(self, other):
        if isinstance(other, Node):
            other = other.coordinates
        return Node(self.coordinates // other)

    def __array__(self):
        return self.coordinates




@dataclass(order=True)
class Edge:
    """An edge in a graph."""
    node_indices: frozenset[int] = field(compare=False)
    weight: int | float = field(default=0.0)
    properties: dict = field(default_factory=dict, compare=False)

    def __post_init__(self):
        if not isinstance(self.properties, dict):
            self.properties = dict(self.properties)
        self.weight = float(self.weight)  # Convert weight to float

    def index_of_other_node(self, current_index: int) -> int:
        """Given one node index, return the other node index."""
        node_indices = list(self.node_indices)
        return node_indices[1] if node_indices[0] == current_index else node_indices[0]

    def __eq__(self, other):
        return self.weight == other.weight and self.node_indices == other.node_indices

    def __repr__(self):
        return f'Edge(weight={self.weight}, node_indices={self.node_indices}, properties={self.properties})'

    def __hash__(self):
        return hash(self.node_indices)

    def __copy__(self):
        return Edge(weight=self.weight, node_indices=self.node_indices, properties=self.properties)

    def __deepcopy__(self, memo: Mapping | None = None):
        return Edge(weight=self.weight, node_indices=self.node_indices, properties=self.properties)



class Graph:
    """A graph."""
    nodes: NodeSequence = field(default_factory=list)
    edges: EdgeSequence = field(default_factory=tuple)
    properties: dict = field(default_factory=dict)
    edge_weight_function: EdgeWeightCallable | None
    heuristic_distance_function: HeuristicDistanceCallable | None

    @classmethod
    def from_edge_definitions(cls, edge_definitions: EdgeDefinitionSequence, properties: dict | None = None, edge_weight_function: EdgeWeightCallable | None = None, heuristic_distance_function: HeuristicDistanceCallable | None = None) -> 'Graph':
        coordinates_of_all_nodes = []

        for edge_definition in edge_definitions:
            for edge_node_coordinates in edge_definition[1]:
                if edge_node_coordinates not in coordinates_of_all_nodes:
                    coordinates_of_all_nodes.append(edge_node_coordinates)

        nodes = dict()
        edges = []

        for edge_definition in edge_definitions:
            indices = []
            for edge_node_coordinates in edge_definition[1]:
                index = coordinates_of_all_nodes.index(edge_node_coordinates)
                indices.append(index)
                nodes[index] = Node(coordinates=edge_node_coordinates)
            node_indices = frozenset(indices)
            edge = Edge(weight=edge_definition[0], node_indices=node_indices)
            edges.append(edge)

        nodes = [nodes[index] for index in sorted(nodes)]

        return cls(nodes=nodes, edges=edges, properties=properties, edge_weight_function=edge_weight_function, heuristic_distance_function=heuristic_distance_function)

    def __init__(self, nodes: NodeSequence, edges: EdgeSequence, properties: dict | None = None, edge_weight_function: EdgeWeightCallable | None = None, heuristic_distance_function: HeuristicDistanceCallable | None = None):
        """Initialize a graph."""
        self.nodes = deepcopy(nodes)
        self.edges = tuple(deepcopy(edge) for edge in edges)
        self.properties = {} if properties is None else (deepcopy(properties) if isinstance(properties, dict) else dict(properties))
        if heuristic_distance_function:
            self.heuristic_distance_function = heuristic_distance_function
        if edge_weight_function:
            self.edge_weight_function = edge_weight_function
            for edge in self.edges:
                edge.weight = self.edge_weight_function(self, edge)

    def __repr__(self):
        return f'Graph(nodes={self.nodes}, edges={self.edges})'

    def __str__(self):
        return f'Graph containing these nodes: {self.nodes} and these edges: {self.edges})'

    def __eq__(self, other):
        return self.nodes == other.nodes and self.edges == other.edges

    def __hash__(self):
        return hash((self.nodes, self.edges))

    def adjacency_map(self) -> AdjacencyMap:
        """Render an adjacency map."""

        adjacency_map = {node: [] for node in self.nodes}

        for edge in self.edges:
            for node_index in edge.node_indices:
                bisect.insort(adjacency_map[self.nodes[node_index]], edge)

        return adjacency_map

    def adjacency_matrix(self) -> np.ndarray:
        """Render an adjacency matrix."""

        adjacency_matrix = np.ones((len(self.nodes), len(self.nodes))) * np.inf

        for edge in self.edges:
            node_indices = list(edge.node_indices)
            adjacency_matrix[node_indices[0], node_indices[1]] = adjacency_matrix[node_indices[1], node_indices[0]] = edge.weight

        return adjacency_matrix



def length_cost_per_unit(graph: Graph, edge: Edge) -> float:
    cost_per_unit = edge.properties['cost_per_unit']
    heuristic_distance = graph.heuristic_distance_function
    attached_nodes = [graph.nodes[node_index] for node_index in edge.node_indices]
    return cost_per_unit * heuristic_distance(attached_nodes[0], attached_nodes[1])


class NoNavigablePathError(Exception):
    """Raised when no path can be found to the goal node."""
    def __init__(self, start_node: Node, goal_node: Node='N/A'):
        super().__init__(f'No path exists between nodes {start_node} and {goal_node}.')
