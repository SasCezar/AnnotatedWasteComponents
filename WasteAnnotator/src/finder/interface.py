from typing import Protocol


class ProjectFinder(Protocol):
    def find_projects(self, amount: int):
        pass
