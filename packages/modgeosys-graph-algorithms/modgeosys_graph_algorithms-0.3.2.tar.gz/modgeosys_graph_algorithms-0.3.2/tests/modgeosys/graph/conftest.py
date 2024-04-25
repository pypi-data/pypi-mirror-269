import pickle
import pytest

from src.modgeosys.graph.distance import manhattan_distance
from src.modgeosys.graph.types import Node, Edge, Graph, length_cost_per_unit


@pytest.fixture
def valid_nodes():
    return [Node(properties={}, coordinates=(0.0, 0.0)), Node(properties={}, coordinates=(0.0, 2.0)), Node(properties={}, coordinates=(1.0, 0.0)), Node(properties={}, coordinates=(2.0, 1.0)), Node(properties={}, coordinates=(2.0, 3.0))]


@pytest.fixture
def valid_edges1():
    return (Edge(properties={}, weight=2, node_indices=frozenset((0, 1))),
            Edge(properties={}, weight=1, node_indices=frozenset((0, 2))),
            Edge(properties={}, weight=1, node_indices=frozenset((2, 3))),
            Edge(properties={}, weight=3, node_indices=frozenset((1, 4))),
            Edge(properties={}, weight=1, node_indices=frozenset((3, 4))))


@pytest.fixture
def valid_edges2():
    return (Edge(properties={}, weight=3, node_indices=frozenset((0, 1))),
            Edge(properties={}, weight=1, node_indices=frozenset((0, 2))),
            Edge(properties={}, weight=1, node_indices=frozenset((2, 3))),
            Edge(properties={}, weight=3, node_indices=frozenset((1, 4))),
            Edge(properties={}, weight=1, node_indices=frozenset((3, 4))))


@pytest.fixture
def valid_edges3():
    return (Edge(properties={'cost_per_unit': 2}, node_indices=frozenset((0, 1))),
            Edge(properties={'cost_per_unit': 1}, node_indices=frozenset((0, 2))),
            Edge(properties={'cost_per_unit': 1}, node_indices=frozenset((2, 3))),
            Edge(properties={'cost_per_unit': 3}, node_indices=frozenset((1, 4))),
            Edge(properties={'cost_per_unit': 1}, node_indices=frozenset((3, 4))))


@pytest.fixture
def valid_graph1(valid_nodes, valid_edges1):
    return Graph(properties={}, nodes=valid_nodes, edges=valid_edges1, heuristic_distance_function=manhattan_distance)


@pytest.fixture
def valid_graph2(valid_nodes, valid_edges2):
    return Graph(properties={}, nodes=valid_nodes, edges=valid_edges2, heuristic_distance_function=manhattan_distance)


@pytest.fixture
def valid_graph3(valid_nodes, valid_edges3):
    return Graph(properties={}, nodes=valid_nodes, edges=valid_edges3, heuristic_distance_function=manhattan_distance, edge_weight_function=length_cost_per_unit)


@pytest.fixture
def valid_graph_from_edge_definitions():
    return Graph.from_edge_definitions(edge_definitions=((2, ((0.0, 0.0), (0.0, 2.0))),
                                                         (1, ((0.0, 0.0), (1.0, 0.0))),
                                                         (1, ((1.0, 0.0), (2.0, 1.0))),
                                                         (3, ((0.0, 2.0), (2.0, 3.0))),
                                                         (1, ((2.0, 1.0), (2.0, 3.0)))),
                                       heuristic_distance_function=manhattan_distance)


@pytest.fixture
def valid_graph_larger():
    with open('data/graph.pickle', 'rb') as pickled_sample_larger_graph_file:
        graph = pickle.load(pickled_sample_larger_graph_file)
        graph.heuristic_distance_function = manhattan_distance
        return graph


@pytest.fixture
def valid_graph_larger_with_string_edge_weights(valid_graph_larger):
    graph = valid_graph_larger
    for edge in graph.edges:
        edge.weight = str(edge.weight)
    return graph