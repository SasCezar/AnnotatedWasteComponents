from typing import Optional, List, Dict, Any, Tuple

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
    nodes: List[Any]
    edges: List[Tuple[Any, Any, Dict[str, Any]]]

    @classmethod
    def from_graph(cls, graph: nx.Graph) -> 'GraphModel':
        edges_with_data = [(u, v, data) for u, v, data in graph.edges(data=True)]
        return cls(
            nodes=list(graph.nodes),
            edges=edges_with_data
        )

    def to_graph(self) -> nx.Graph:
        graph = nx.Graph()
        graph.add_nodes_from(self.nodes)
        # Add edges along with their attributes
        for u, v, data in self.edges:
            graph.add_edge(u, v, **data)
        return graph


class Project(BaseModel):
    """
    Class defining a project. Each project has a name, a remote (url) and a list of files.
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
    communities: Optional[Dict[str, Dict[str, int]]] = None
