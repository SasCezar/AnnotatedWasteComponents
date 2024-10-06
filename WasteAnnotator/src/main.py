from typing import List

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

from annotator import AutoFLAnnotator
from community import CommunityExtractor
from graphextractor import ArcanGraphExtractor
from pipeline import CompletePipeline
from exporter import JSONProjectExporter, ProjectExporter
from finder import GitHubFinder


@hydra.main(config_path="../config/", config_name="main.yaml", version_base='1.3')
def run(cfg: DictConfig):
    finder: GitHubFinder = instantiate(cfg.finder)
    graph_extractor: ArcanGraphExtractor = instantiate(cfg.graphextractor)
    semantic_annotator = instantiate(cfg.annotator)
    community_extractor = instantiate(cfg.community)
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
