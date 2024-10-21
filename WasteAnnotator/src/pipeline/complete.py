from typing import Dict, Union
from urllib.error import HTTPError

from loguru import logger
from joblib import Parallel, delayed
from tqdm import tqdm

from annotator import Annotator
from communityextractor import CommunityExtractor
from exporter import ProjectExporter
from finder import ProjectFinder
from graphextractor.interface import GraphExtractor
from loader import ProjectLoader


class CompletePipeline:
    """
    The CompletePipeline class is responsible for running the complete pipeline to annotate projects.
    """

    def __init__(self,
                 project_finder: ProjectFinder,
                 project_loader: Union[ProjectLoader, None],
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
        self.project_loader: Union[ProjectLoader, None] = project_loader
        self.graph_extractor: GraphExtractor = graph_extractor
        self.semantic_annotator: Annotator = semantic_annotator
        self.community_extractor: CommunityExtractor = community_extractor
        self.project_exporter: Dict[str, ProjectExporter] = project_exporter

        logger.info(f"Initialized ComponentAnnotator")

    def process_project(self, project):
        """
        Processes a single project by annotating, extracting graphs, and exporting the results.
        """
        try:
            if self.project_loader:
                project = self.project_loader.load(project)


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
                logger.info(f"Exporting project `{project.name}` using {exporter}")
                self.project_exporter[exporter].export(project)
            logger.info(f"Finished exporting project `{project.name}`")

        except RuntimeError as exc:
            logger.error(f"{exc}")
        except ValueError as exc:
            logger.error(f"{exc}")
        except Exception as exc:
            logger.error(f"Unexpected error occurred while processing `{project.name}`: {exc}")

    def run(self, num_proj: int = 10, n_jobs: int = -1):
        """
        Runs the pipeline in parallel for the specified number of projects using joblib, with tqdm for progress.

        Args:
            num_proj (int): Number of projects to retrieve and process.
            n_jobs (int): Number of parallel jobs to run (-1 means using all available processors).
        """
        try:
            logger.info("Starting to retrieve abandoned projects from GitHub")
            abandoned_projects = self.project_finder.find_projects(num_proj)
            logger.info("Finished retrieving abandoned projects from GitHub")
        except HTTPError as exc:
            logger.error("Failed to retrieve abandoned projects from GitHub")
            return

        # Wrap the iterable in tqdm for a progress bar
        logger.info(f"Processing {len(abandoned_projects)} projects in parallel with {n_jobs} jobs.")
        Parallel(n_jobs=n_jobs)(
            delayed(self.process_project)(project) for project in tqdm(abandoned_projects, desc="Processing projects", unit="project")
        )
        logger.info("Finished processing projects")