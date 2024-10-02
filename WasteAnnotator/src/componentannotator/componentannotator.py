from typing import List, Tuple, Dict

import numpy as np
import pandas as pd
import requests
from loguru import logger

from entities import File, Project


def get_label(distribution, taxonomy):
    """
    Returns the label for a given distribution and taxonomy.

    Args:
        distribution:
        taxonomy:

    Returns:
        The label for the distribution and taxonomy.
    """
    return taxonomy[str(np.argmax(distribution))]


class ComponentAnnotator:
    """
    The ComponentAnnotator class is responsible for annotating files in abandoned GitHub projects.
    It utilizes the ProjectExtractor to find abandoned projects, the ComponentExtractor to run the
    Arcan tool for component information, and the auto-fl annotator for file-level annotations (weak labels).
    """

    def __init__(self, language: str = "java"):
        """
        Initializes the ComponentAnnotator with default values for the ProjectExtractor.

        Args:
            language: The programming language used in the project.
        """
        self.language = language

        logger.info(f"Initialized ComponentAnnotator (project programming language -> {language})")

    def annotate_project(self, project: Project) -> Project:
        """
        Annotate a single GitHub project
        then runs the arcan tool (encapsulated in component_extractor) to get component information
        and in after that runs the annotator (auto-fl) to get file level annotations (weak labels)
        for all the files in the project.

        Returns:
            pd.DataFrame: pd.DataFrame: Dataframe containing files in the project with component and component-label information.
        """
        logger.info(f"Retrieving and annotating components of project `{project.name}`")

        file_annot = self._annotate_file(project.name, project.remote)  # Failed? Then this returns empty DataFrame.

        if not file_annot:
            raise RuntimeError(f"AutoFL failed to annotate project {project.name}.")

        project.files = file_annot
        return project

    def _annotate_file(self, project_name: str, remote: str) -> Dict[str, File]:
        """
        Request to auto-fl to annotate a GitHub project.

        Args:
            project_name: Name of the GitHub project.
            remote: HTML URL of the GitHub project.

        Returns:
            pd.DataFrame: A pandas DataFrame containing information about annotated files.

        Notes:
            - Only Java projects are fully supported and tested with the auto-fl annotator.
        """
        url = 'http://auto-fl:8000/label/files'
        analysis = {
            "name": project_name,  # "Waikato|weka-3.8",
            "remote": remote,  # "https://github.com/Waikato/weka-3.8",
            "languages": [self.language]  # ["java"]
        }

        res = requests.post(url, json=analysis)
        res = res.json()['result']
        taxonomy = res['taxonomy']
        fs = res['versions'][0]['files']
        files: Dict[str, File] = {key: File(**fs[key]) for key in fs}

        return files
