import shutil
import networkx as nx
from os.path import join, exists
from pathlib import Path
from shlex import quote
from subprocess import call

import hydra
import pandas as pd
from loguru import logger
import os
from omegaconf import DictConfig


class ComponentExtractor:
    def __init__(self):
        self.arcan_graphs: str = ""
        self.arcan_script: str = "/component-annotator/src/arcan/run-arcan.sh"           # NOTE: arcan.bat should be run on Windows
        self.arcan_path: str = "/component-annotator/src/arcan"
        self.repository_path: str = "/component-annotator/data/raw"
        self.arcan_out: str = "/component-annotator/data/arcan-out"
        self.logs_path: str = "/component-annotator/data/arcan-log"

        self.component_graph = None

    def component_graph(self, project: str, language = "JAVA"):
        self.run_arcan(project, language)
        return nx.read_graphml(self.arcan_out)

    """
    Run arcan
    """
    def check_status(self, path) -> bool:
        """
        Checks if the project has already been processed.
        :param path:
        :return:
        """
        return exists(path)

    def run_arcan(self, project: str, language) -> None:
        """
        Runs the script to extract the graphs using Arcan. It also checks if the project has already been processed,
         and if so, it skips it.
        :param cfg:
        :param project:
        :param language:
        :return:
        """

        # What is the point of this line? Is project a GitHub URL string?
        check_path = join(self.arcan_graphs, project.replace('/', '|'), '.completed')
        completed = self.check_status(check_path)
        try:
            if completed:
                logger.info(f"Skipping {project} as it has already been processed")
                return

            command = [self.arcan_script]

            args = [project, quote(project.replace('/', '|')),
                    language, self.arcan_path, self.repository_path, self.arcan_out, join(self.logs_path, 'arcan')]

            command.extend(args)

            logger.info(f"Running command: {' '.join(command)}")

            call(" ".join(command), shell=True)

            if not completed:
                with open(check_path, 'wt') as outf:
                    logger.info(f"Creating file {outf.name}")

            logger.info(f"Finished to extract graph for {project}")

        except Exception as e:
            logger.error(f"Failed to extract graph for {project}")
            logger.error(f"{e}")

        finally:
            if not completed:
                logger.info(f"Cleaning up {project} repository")
                repo_path = join(self.repository_path, project.replace('/', '|'))
                shutil.rmtree(repo_path, ignore_errors=True)
            return

    # @hydra.main(config_path="../conf", config_name="main", version_base="1.2")
    # def extract_graph(self, cfg: DictConfig):
    #     """
    #     Extracts graph from a project including the git history (augmented data).
    #     :param cfg:
    #     :return:
    #     """
    #     projects = pd.read_csv(cfg.dataset)
    #     if 'language' not in projects:
    #         projects['language'] = [cfg.language] * len(projects)
    #
    #     projects['language'] = projects['language'].str.upper()
    #     projects = projects[projects['language'] == cfg.language.upper()]
    #     languages = projects['language']
    #     projects = projects['full_name']
    #
    #     logger.info(f"Extracting graphs for {len(projects)} projects")
    #
    #     Path(join(cfg.logs_path, 'arcan')).mkdir(parents=True, exist_ok=True)
    #     if cfg.num_workers > 1:
    #         logger.info(f"Using {cfg.num_workers} workers")
    #         from multiprocessing import Pool
    #         with Pool(cfg.num_workers) as p:
    #             p.starmap(self.run_arcan, zip([cfg] * len(projects), projects, languages))
    #     else:
    #         for i, (project, language) in enumerate(zip(projects, languages)):
    #             logger.info(f"Extracting features for {project} - Progress: {(i + 1) / len(projects) * 100:.2f}%")
    #             self.run_arcan(cfg, project, language)
