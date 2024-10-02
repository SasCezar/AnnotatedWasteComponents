from typing import Callable, List

from entities import Project


class CommunityExtractor:
    def __init__(self, algorithms: List[Callable]):
        self.algorithms = algorithms

    def extract(self, project: Project) -> Project:
        # Extract components/communities from the dependency graph.

        for algo, fn in self.algorithms:
            communities = fn(project.dep_graph.to_graph())
            project.communities[algo] = communities

        return project