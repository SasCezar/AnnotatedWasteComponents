import logging
from typing import Callable, Dict, Any

from cdlib import NodeClustering
from loguru import logger

from entities import Project

def community_to_dict(node_clustering: NodeClustering) -> Dict[Any, int]:
    node_community_dict = {}

    # Loop through each community and its corresponding nodes
    for community_id, community in enumerate(node_clustering.communities):
        for node in community:
            node_community_dict[node] = community_id

    return node_community_dict

class CommunityExtractor:
    """
    The CommunityExtractor class is responsible for extracting communities from the dependency graph.
    """

    def __init__(self, algorithms: Dict[str, Callable] = None,
                 force_run: bool = False):
        """
        Initializes the CommunityExtractor instance.
        Args:
            algorithms: List of algorithms to extract communities from the dependency graph.
        """
        if not algorithms:
            logging.warning("No community detection algorithms provided. Using default Louvain algorithm.")
            algorithms = {'louvain': {'function': 'cdlib.algorithms.louvain'}}
        self.algorithms: Dict[str, Callable] = algorithms
        self.force_run: bool = force_run

        print(self.algorithms)

        logger.info("Initialized CommunityExtractor")

    def extract(self, project: Project) -> Project:
        # Extract components/communities from the dependency graph.
        logging.info("Extracting communities from the dependency graph")

        for algo in self.algorithms:
            logging.info(f"Extracting communities using {algo} algorithm")

            if algo in project.communities and not self.force_run:
                logging.info(f"Communities already extracted using {algo} algorithm. Skipping.")
                continue

            fn = self.algorithms[algo]
            communities: NodeClustering = fn(project.dep_graph.to_graph())
            project.communities[algo] = community_to_dict(communities)

        return project
