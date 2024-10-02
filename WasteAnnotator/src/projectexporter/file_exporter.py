from pathlib import Path

from projectexporter.exporter import ProjectExporter


class JSONProjectExporter(ProjectExporter):
    def __init__(self, out_dir, exclude_keys=None):
        super().__init__()
        self.file_extension = "json"
        self.out_dir = Path(out_dir)
        if exclude_keys is None:
            exclude_keys = {}
        self.exclude_keys = exclude_keys


    def export(self, project):
        with open(self.out_dir / f'{project.name}.{self.file_extension}', 'w') as file:
            file.write(project.model_dump_json(exclude=self.exclude_keys))