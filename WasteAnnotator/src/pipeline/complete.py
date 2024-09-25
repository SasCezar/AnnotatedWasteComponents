from urllib.error import HTTPError

from loguru import logger

from componentaggregator.componentaggregator import ComponentAggregator
from componentannotator.componentannotator import ComponentAnnotator
from componentextractor.componentextractor import ComponentExtractor
from projectextractor.projectextractor import ProjectExtractor


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
                 component_aggregator: ComponentAggregator,
                 language):
        """
        Initializes the ComponentAnnotator with default values for the ProjectExtractor.

        Args:
            language: The programming language used in the project.
        """
        self.project_extractor: ProjectExtractor = project_extractor
        self.component_extractor: ComponentExtractor = component_extractor
        self.component_annotator: ComponentAnnotator = component_annotator
        self.component_aggregator: ComponentAggregator = component_aggregator
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
            project_name = project["name"]
            project_url = project["html_url"]
            try:
                file_annotation = self.component_annotator.annotate_project(project_name, project_url)


                components = self.component_extractor.set_project(project_name, project_url).infomap_components()
                # component_extractor handles arcan failed exceptions.
                dep_graph = self.component_extractor.dependency_graph()

                self.component_aggregator.set_state(components, file_annotation, dep_graph, project_name)

                # Dataframe contains component identifier and component label for each file.
                df_components = self.component_aggregator.create_aggregate()
                logger.info(f"Finished annotating components of project `{project_name}`")
            except RuntimeError as exc:
                logger.error(f"{exc}")
                continue
