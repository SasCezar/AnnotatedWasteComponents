from asyncio import Protocol

from entities import Project


class Annotator(Protocol):

    def annotate_project(self, project: Project) -> Project:
        pass