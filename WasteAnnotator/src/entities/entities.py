from typing import Optional, List, Dict, Any

import networkx as nx
from pydantic import BaseModel


class Annotation(BaseModel):
    """
    Class defining the annotation assigned to a file.
    """
    distribution: List[float]
    unannotated: bool


class File(BaseModel):
    """
    Class defining a file. Each file has a path, a language, a content, a list of identifiers and a package.
    """
    path: str
    language: str
    content: Optional[str] = None
    identifiers: Optional[List[str]] = None
    package: Optional[str] = None
    annotation: Optional[Annotation] = None


class GraphModel(BaseModel):
    nodes: Dict[Any, Dict[str, Any]]
    edges: List[List[Any]]  # List of [u, v, data] for edge representation

    @classmethod
    def from_graph(cls, graph: nx.Graph) -> 'GraphModel':
        # Collect nodes with their data as a dictionary
        nodes_with_data = {node: data for node, data in graph.nodes(data=True)}
        # Collect edges as a list of lists [u, v, data]
        edges_with_data = [[u, v, data] for u, v, data in graph.edges(data=True)]
        # file_to_node = {data['filePathRelative']: node for node, data in nodes_with_data.items()}
        return cls(
            nodes=nodes_with_data,
            edges=edges_with_data,
        )

    def to_graph(self) -> nx.Graph:
        graph = nx.Graph()
        # Add nodes along with their attributes from the dictionary
        for node, data in self.nodes.items():
            graph.add_node(node, **data)
        # Add edges from the list of [u, v, data]
        for u, v, data in self.edges:
            graph.add_edge(u, v, **data)
        return graph



class Project(BaseModel):
    """
    Class defining a project. Each project has a name, a remote, a description, a number of stargazers, a language,
    a flag indicating if it is archived, a date of last push, a list of files, a dependency graph and a list of
    communities.
    """
    name: str
    remote: str
    description: Optional[str] = None
    stargazers_count: Optional[int] = None
    language: Optional[str] = None
    archived: Optional[bool] = None
    pushed_at: Optional[str] = None
    files: Optional[Dict[str, File]] = None
    dep_graph: Optional[GraphModel] = None
    communities: Optional[Dict[str, Dict[Any, int]]] = {}
