from abc import ABC, abstractmethod

from entities import Project


class ProjectExporter(ABC):
    """
    The ProjectExporter class is responsible for exporting annotated projects to a specific format.
    """

    @abstractmethod
    def export(self, project: Project):
        """
        Exports the annotated project to a specific format.

        Args:
            project: The annotated project to be exported.
        """
        pass