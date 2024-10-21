import json
from pathlib import Path
from typing import Union

from loguru import logger

from entities import Project


class ProjectLoader:
    def __init__(self, projects_path: Union[str, Path], extension: str = 'json'):
        self.project_paths: Path = Path(projects_path)
        self.extension: str = extension

    def load(self, project: Project) -> Project:
        project_file = self.project_paths / f"{project.name}.{self.extension}"
        if not project_file.exists():
            logger.info(f"Project `{project.name}` not found in path `{self.project_paths}`")
            return project

        logger.info(f"Found project `{project.name}`. Loading from file `{project_file}`")
        with open(project_file, 'r') as f:
            project = Project(**json.load(f))

        return project