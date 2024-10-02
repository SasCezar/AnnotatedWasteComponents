from typing import List

from componentannotator import ComponentAnnotator
from componentextractor import CommunityExtractor
from componentextractor import ComponentExtractor
from pipeline.complete import CompletePipeline
from projectexporter import JSONProjectExporter, ProjectExporter
from projectextractor import ProjectExtractor

if __name__ == "__main__":
    JAVA = "java"
    exporter: List[ProjectExporter] = [JSONProjectExporter('/waste-annotator/data/annotated/')]
    CompletePipeline(
        ProjectExtractor(100, "2021-01-01", language=JAVA),
        ComponentExtractor(language=JAVA),
        ComponentAnnotator("java"),
        CommunityExtractor([]),
        exporter,
        language=JAVA
    ).run()
