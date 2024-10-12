from typing import Dict
from urllib.error import HTTPError

from loguru import logger

from annotator import Annotator
from communityextractor import CommunityExtractor
from exporter import ProjectExporter
from finder import ProjectFinder
from graphextractor.interface import GraphExtractor


class CompletePipeline:
    """
    The CompletePipeline class is responsible for running the complete pipeline to annotate projects.
    """

    def __init__(self,
                 project_finder: ProjectFinder,
                 graph_extractor: GraphExtractor,
                 semantic_annotator: Annotator,
                 community_extractor: CommunityExtractor,
                 project_exporter: Dict[str, ProjectExporter]
                 ):
        """

        Args:
            project_finder:
            graph_extractor:
            semantic_annotator:
            community_extractor:
            project_exporter:
        """

        self.project_finder: ProjectFinder = project_finder
        self.graph_extractor: GraphExtractor = graph_extractor
        self.semantic_annotator: Annotator = semantic_annotator
        self.community_extractor: CommunityExtractor = community_extractor
        self.project_exporter: Dict[str, ProjectExporter] = project_exporter

        logger.info(f"Initialized ComponentAnnotator")

    def run(self, num_proj: int = 10):
        abandoned_projects = []
        try:
            logger.info("Starting to retrieve abandoned projects from GitHub")
            abandoned_projects = self.project_finder.find_projects(num_proj)
            logger.info("Finished retrieving abandoned projects from GitHub")
        except HTTPError as exc:
            logger.error("Failed to retrieve abandoned projects from GitHub")

        for project in abandoned_projects:

            try:
                logger.info(f"Starting to annotate project `{project.name}`")
                project = self.semantic_annotator.annotate_project(project)
                logger.info(f"Finished annotating project `{project.name}`")

                logger.info(f"Starting to extract dependency graph for project `{project.name}`")
                project = self.graph_extractor.extract_graph(project)
                logger.info(f"Finished extracting dependency graph for project `{project.name}`")

                logger.info(f"Starting to extract community information for project `{project.name}`")
                project = self.community_extractor.extract(project)
                logger.info(f"Finished extracting community information for project `{project.name}`")

                logger.info(f"Starting to export project `{project.name}`")
                for exporter in self.project_exporter:
                    logger.info(f"Exporting project `{project.name}` using {exporter.__class__.__name__}")
                    self.project_exporter[exporter].export(project)
                logger.info(f"Finished exporting project `{project.name}`")


            except RuntimeError as exc:
                logger.error(f"{exc}")
                continue
            except ValueError as exc:
                logger.error(f"{exc}")
                continue
