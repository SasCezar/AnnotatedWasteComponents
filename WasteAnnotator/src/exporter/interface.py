from typing import Protocol

from entities import Project


class ProjectExporter(Protocol):
    """
    The ProjectExporter class is responsible for exporting annotated projects to a specific format.
    """

    def export(self, project: Project):
        """
        Exports the annotated project to a specific format.

        Args:
            project: The annotated project to be exported.
        """
        pass