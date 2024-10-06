import logging
from typing import Callable, Dict, Union

from hydra.utils import call
from loguru import logger

from entities import Project


class CommunityExtractor:
    """
    The CommunityExtractor class is responsible for extracting communities from the dependency graph.
    """

    def __init__(self, algorithms: Dict[str, Dict[str, Union[Callable, Dict]]] = None,
                 force_run: bool = False):
        """
        Initializes the CommunityExtractor instance.
        Args:
            algorithms: List of algorithms to extract communities from the dependency graph.
        """
        if not algorithms:
            logging.warning("No community detection algorithms provided. Using default Louvain algorithm.")
            algorithms = {'louvain': {'function': 'cdlib.algorithms.louvain'}}
        self.algorithms = algorithms
        self.force_run = force_run

        print(self.algorithms)

        logger.info("Initialized CommunityExtractor")

    def extract(self, project: Project) -> Project:
        # Extract components/communities from the dependency graph.

        for algo in self.algorithms:
            logging.info(f"Extracting communities using {algo} algorithm")
            if algo in project.communities and not self.force_run:
                logging.info(f"Communities already extracted using {algo} algorithm. Skipping.")
                continue
            f = self.algorithms[algo]
            fn = f['function']
            kwargs = f['kwargs'] if 'kwargs' in f else {}
            communities = call(target=fn, *[project.dep_graph.to_graph()], **kwargs)
            project.communities[algo] = communities

        return project
