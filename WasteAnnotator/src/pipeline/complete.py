from typing import List
from urllib.error import HTTPError

from loguru import logger

from projectexporter import ProjectExporter
from projectextractor import ProjectExtractor

from componentannotator import ComponentAnnotator
from componentextractor import CommunityExtractor
from componentextractor import ComponentExtractor


class CompletePipeline:
    """
    The ComponentAnnotator class is responsible for annotating files in abandoned GitHub projects.
    It utilizes the ProjectExtractor to find abandoned projects, the ComponentExtractor to run the
    Arcan tool for component information, and the auto-fl annotator for file-level annotations (weak labels).
    """

    def __init__(self,
                 project_extractor: ProjectExtractor,
                 component_extractor: ComponentExtractor,
                 component_annotator: ComponentAnnotator,
                 community_extractor: CommunityExtractor,
                 project_exporter: List[ProjectExporter],
                 language):
        """
        Initializes the ComponentAnnotator with default values for the ProjectExtractor.

        Args:
            language: The programming language used in the project.
        """
        self.project_extractor: ProjectExtractor = project_extractor
        self.component_extractor: ComponentExtractor = component_extractor
        self.component_annotator: ComponentAnnotator = component_annotator
        self.community_extractor: CommunityExtractor = community_extractor
        self.project_exporter: List[ProjectExporter] = project_exporter
        self.language: str = language

        logger.info(f"Initialized ComponentAnnotator (project programming language -> {language})")

    def run(self, num_proj: int = 10):
        abandoned_projects = []
        try:
            abandoned_projects = self.project_extractor.find_abandoned_projects(num_proj)
            logger.info("Finished retrieving abandoned projects from GitHub")
        except HTTPError as exc:
            logger.error("Failed to retrieve abandoned projects from GitHub")

        for project in abandoned_projects:

            try:
                project = self.component_extractor.dependency_graph(project)

                project = self.component_annotator.annotate_project(project)

                logger.info(f"Finished annotating components of project `{project.name}`")

                for exporter in self.project_exporter:
                    exporter.export(project)
            except RuntimeError as exc:
                logger.error(f"{exc}")
                continue
            except ValueError as exc:
                logger.error(f"{exc}")
                continue