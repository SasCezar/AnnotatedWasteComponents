from collections import Counter

import numpy as np


class SimpleStats:
    @staticmethod
    def stats(project: dict):
        """
        Args:
            project (dict): The project dictionary.
        """
        stats = {
            "num_files": len(project),
            "num_components": max([project[file]["component"] for file in project]),
            "num_packages": len(({project[file]["package"] for file in project})),
            "distinct_labels": len({project[file]["label"] for file in project})
        }


        stats["avg_file_component"] = np.mean(list(Counter([project[file]["component"] for file in project]).values()))
        stats["std_file_component"] = np.std(list(Counter([project[file]["component"] for file in project]).values()))
        return stats
