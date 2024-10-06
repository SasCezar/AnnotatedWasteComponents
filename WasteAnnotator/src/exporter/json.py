from pathlib import Path

from entities import Project
from exporter.interface import ProjectExporter


class JSONProjectExporter(ProjectExporter):
    """
    The JSONProjectExporter class is responsible for exporting annotated projects to a JSON format.
    Uses the pydantic model_dump_json method to dump the project to a JSON string.
    """
    def __init__(self, out_dir, exclude_keys=None):
        """
        Initializes the JSONProjectExporter instance.
        Args:
            out_dir: Output directory to save the JSON file.
            exclude_keys: List of keys to exclude from the JSON dump.
        """
        super().__init__()
        self.file_extension = "json"
        self.out_dir = Path(out_dir)
        if exclude_keys is None:
            exclude_keys = {}
        self.exclude_keys = exclude_keys


    def export(self, project: Project):
        with open(self.out_dir / f'{project.name}.{self.file_extension}', 'w') as file:
            file.write(project.model_dump_json(exclude=self.exclude_keys))