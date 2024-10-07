from typing import Dict

import numpy as np
import pandas as pd
import requests
from loguru import logger

from annotator.interface import Annotator
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


class AutoFLAnnotator(Annotator):
    """
    Annotate the project with semantic labels using the AutoFL tool. The AutoFL tool is a weak label annotator that
    provides multi-granular (file, package, project) domain application labels.
    """

    def __init__(self, endpoint: str = "http://auto-fl:8000/label/files"):
        """

        Args:
            endpoint:
        """
        super().__init__()
        self.endpoint = endpoint

        logger.info(f"Initialized AutoFL annotator")

    def annotate_project(self, project: Project) -> Project:
        """
        Annotate the components of a project with semantic labels.
        Args:
            project: The project to annotate.

        Returns:
            Project: The annotated project
        """
        logger.info(f"Retrieving and annotating components of project `{project.name}`")

        file_annot = self._annotate_file(project.name, project.remote,
                                         project.language)  # Failed? Then this returns empty DataFrame.

        if not file_annot:
            raise RuntimeError(f"AutoFL failed to annotate project {project.name}.")

        project.files = file_annot
        return project

    def _annotate_file(self, project_name: str, remote: str, language: str) -> Dict[str, File]:
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
        analysis = {
            "name": project_name,  # "Waikato|weka-3.8",
            "remote": remote,  # "https://github.com/Waikato/weka-3.8",
            "languages": [language]  # ["java"]
        }

        res = requests.post(self.endpoint, json=analysis)
        res = res.json()['result']
        taxonomy = res['taxonomy']
        fs = res['versions'][0]['files']
        files: Dict[str, File] = {key: File(**fs[key]) for key in fs}

        return files
