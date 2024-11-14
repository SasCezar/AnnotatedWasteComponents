from typing import Protocol

import networkx as nx


class GraphCleaner(Protocol):
    def clean(self, graph: nx.Graph) -> nx.Graph:
        pass


class ArcanGraphCleaner:
    def __init__(self, edges_type_remove: list):
        self.edges_type_remove = edges_type_remove

    def clean(self, graph: nx.Graph):
        """
        Remove nodes and edges from the graph based on their type.
        """
        # Set 'weight' attribute for edges based on 'Weight' attribute
        nx.set_edge_attributes(graph, {e: data['Weight'] for e, data in graph.edges.items() if 'Weight' in data}, 'weight')


        # Delete vertices where the name contains a '$'
        nodes_to_remove = [n for n, data in graph.nodes(data=True) if '$' in data['name']]
        graph.remove_nodes_from(nodes_to_remove)

        # Delete edges that match any label in clean_edges
        edges_to_remove = [(u, v) for u, v, data in graph.edges(data=True) if data.get('labelE') in self.edges_type_remove]
        graph.remove_edges_from(edges_to_remove)

        # Remove nodes with degree 0 (isolated nodes)
        isolated_nodes = list(nx.isolates(graph))
        graph.remove_nodes_from(isolated_nodes)

        return graph