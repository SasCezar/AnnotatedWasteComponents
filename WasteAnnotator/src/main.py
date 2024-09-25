from componentaggregator.componentaggregator import ComponentAggregator
from componentannotator.componentannotator import ComponentAnnotator
from componentextractor.componentextractor import ComponentExtractor
from pipeline.complete import CompletePipeline
from projectextractor.projectextractor import ProjectExtractor

if __name__ == "__main__":
    JAVA = "java"
    CompletePipeline(
        ProjectExtractor(100, "2021-01-01", language=JAVA),
        ComponentExtractor(language=JAVA),
        ComponentAnnotator("java"),
        ComponentAggregator(),
        language=JAVA
    ).run()
