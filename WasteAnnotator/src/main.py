from typing import List

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

from annotator import Annotator
from community import CommunityExtractor
from exporter import ProjectExporter
from finder import ProjectFinder
from graphextractor.interface import GraphExtractor
from pipeline import CompletePipeline


@hydra.main(config_path="../config/", config_name="main.yaml", version_base='1.3')
def run(cfg: DictConfig):
    finder: ProjectFinder = instantiate(cfg.finder)
    graph_extractor: GraphExtractor = instantiate(cfg.graphextractor)
    semantic_annotator: Annotator = instantiate(cfg.annotator)
    community_extractor: CommunityExtractor = instantiate(cfg.community)
    exporter: List[ProjectExporter] = instantiate(cfg.exporter)
    CompletePipeline(
        finder,
        graph_extractor,
        semantic_annotator,
        community_extractor,
        exporter,
    ).run()


if __name__ == "__main__":
    run()
