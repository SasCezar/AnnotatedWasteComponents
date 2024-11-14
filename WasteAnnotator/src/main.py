from typing import Dict

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig

from annotator import Annotator
from communityextractor import CommunityExtractor
from exporter import ProjectExporter
from finder import ProjectFinder
from graphextractor import GraphExtractor
from loader import ProjectLoader
from pipeline import CompletePipeline
from utils import instantiate_community_extractors


@hydra.main(config_path="../config/", config_name="main.yaml", version_base='1.3')
def run(cfg: DictConfig):
    finder: ProjectFinder = instantiate(cfg.finder)
    loader: ProjectLoader = instantiate(cfg.loader)
    graph_extractor: GraphExtractor = instantiate(cfg.graphextractor)
    semantic_annotator: Annotator = instantiate(cfg.annotator)

    community_extractor: CommunityExtractor = CommunityExtractor(instantiate_community_extractors(cfg.community))

    exporter: Dict[str, ProjectExporter] = instantiate(cfg.exporter)

    CompletePipeline(
        finder,
        loader,
        graph_extractor,
        semantic_annotator,
        community_extractor,
        exporter,
    ).run(cfg.num_projects, cfg.n_jobs)


if __name__ == "__main__":
    run()
