from typing import Protocol

from entities import Project


class GraphExtractor(Protocol):
    def extract_graph(self, project: Project) -> Project:
        pass