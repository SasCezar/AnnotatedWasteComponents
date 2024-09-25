import traceback
from typing import List, Tuple

import numpy as np
import pandas as pd
import requests
from loguru import logger
from requests import HTTPError


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

    def annotate_project(self, project_name, project_url) -> pd.DataFrame:
        """
        Annotate a single GitHub project
        then runs the arcan tool (encapsulated in component_extractor) to get component information
        and in after that runs the annotator (auto-fl) to get file level annotations (weak labels)
        for all the files in the project.

        Returns:
            pd.DataFrame: pd.DataFrame: Dataframe containing files in the project with component and component-label information.
        """
        logger.info(f"Retrieving and annotating components of project `{project_name}`")

        file_annot = self._annotate_file(project_name, project_url)     # Failed? Then this returns empty DataFrame.
        if file_annot.empty:
            raise RuntimeError("Auto-fl failed to annotate project.")

        return file_annot


    def annotate_project_list(self, projects: List[Tuple]) -> List[pd.DataFrame]:
        """
        See annotate_projects. Difference here is that projects is a list of tuples.

        Args:
            projects (List[Tuple]): (project name, project html url) pairs.

        Returns:
            List[pd.DataFrame]: For each project annotations for the project including component annotations
        """
        df_components_list = []

        for project_name, project_url in projects:
            try:
                df_components_list.append(self.annotate_project(project_name, project_url))
            except RuntimeError as exc:
                logger.error(f"{exc}")
            except ValueError as exc:
                logger.error(f"{exc}")

        return df_components_list


    def _annotate_file(self, project_name: str, remote: str) -> pd.DataFrame:
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
        file_entries = []
        files = res['versions'][0]['files']
        for file_name in files:
            file = files[file_name]
            file_entries.append({
                "path": file["path"],
                "package": file["package"],
                "distribution": file["annotation"]["distribution"],
                "unannotated": file["annotation"]["unannotated"],
                "label": get_label(file["annotation"]["distribution"], taxonomy)
            })

        file_annot = pd.DataFrame(file_entries)
        # Skip package and project level annotations
        return file_annot