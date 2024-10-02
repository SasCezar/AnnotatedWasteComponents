import os
from os.path import join, exists
from subprocess import call

import networkx as nx
from loguru import logger
import shlex

from entities import Project, GraphModel


def check_status(path) -> bool:
    """
    Checks if the project has already been processed.

    Args:
        path: The path to check.

    Returns:
        bool: True if the project has been processed; False otherwise.
    """
    return exists(path)


def arcan_language_str(language: str) -> str:
    """
    Returns the language string that is compatible with Arcan.

    NOTE: Extend this if needed.

    Args:
        language: The language string for auto-fl.

    Returns:
        The language string for Arcan.
    """
    if language in ["JAVA", "CPP", "C", "ASML", "CSHARP", "PYTHON"]:
        return language

    if language == "C++":
        language = "CPP"
    elif language == "C#":
        language = "CSHARP"

    return language.upper()


def find_file_by_extension(directory: str, target_extension: str) -> str:
    """
    Find a file in the specified directory with the given extension.

    Args:
        directory (str): The path to the directory.
        target_extension (str): The target extension to search for.

    Returns:
        str: The filename if a matching file is found, otherwise, an empty string.
    """
    for filename in os.listdir(directory):
        if filename.endswith(target_extension):
            return filename

    raise ValueError(f"No file with extension {target_extension} found in {directory}")


class ComponentExtractor:
    """
    The ComponentExtractor class is responsible for extracting component graphs using the Arcan tool.
    """

    def __init__(self, language: str,
                 arcan_path: str = "/waste-annotator/src/arcan",
                 repository_path: str = "/waste-annotator/data/repository",
                 arcan_out: str = "/waste-annotator/data/",
                 logs_path: str = "/waste-annotator/data/arcan-log",
                 force_run: bool = False
                 ):
        """
        Initializes the ComponentExtractor instance.

        Args:
            language: The programming language of the project.
        """
        self.arcan_graphs: str = ""
        self.arcan_script: str = arcan_path + "/run-arcan.sh"  # NOTE: arcan.bat should be run on Windows
        self.arcan_path: str = arcan_path
        self.repository_path: str = repository_path
        self.arcan_out: str = arcan_out
        self.logs_path: str = logs_path
        self.language: str = arcan_language_str(language)
        self.force_run = force_run

    def dependency_graph(self, project: Project) -> Project:
        """
        Returns the dependency graph for a given project.

        Returns:
            nx.Graph: The dependency graph.
        """
        try:
            dep_graph = self._init_dep_graph(project)
        except:
            raise ValueError(
                f"Failed to extract dependency graph for {project.name}. Arcan might have failed execution.")
        project.dep_graph = GraphModel.from_graph(dep_graph)
        return project

    def _init_dep_graph(self, project: Project) -> nx.Graph:
        directory: str = self.arcan_out + "arcanOutput/" + project.name + "/"
        if not exists(directory) or self.force_run:
            if self.force_run:
                logger.info(f"Force running Arcan for {project.name}")

            self._run_arcan(project.name, project.remote)

        if not os.path.exists(directory):
            raise ValueError(
                "ComponentExtractor illegal state -> project directory cannot be found. Arcan might have failed execution",
                directory)

        file = find_file_by_extension(directory, ".graphml")
        dep_graph = nx.read_graphml(directory + file)
        return dep_graph

    def _run_arcan(self, name, url) -> None:
        """
        Runs the script to extract the graphs using Arcan.
        """

        try:

            command = [self.arcan_script]

            args = [url, name,
                    self.language, self.arcan_path, self.repository_path, self.arcan_out, join(self.logs_path, 'arcan')]

            command.extend(args)

            logger.info(f"Running command: {shlex.join(command)}")

            call(shlex.join(command), shell=True)

            logger.info(f"Finished to extract graph for {name}")

        except Exception as e:
            logger.error(f"Failed to extract graph for {name}")
            logger.error(f"{e}")
            raise e
