import json
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from entities import Project

if __name__ == '__main__':
    projects_dir = Path("../../data/annotated")

    rows = []
    for project_path in tqdm(projects_dir.iterdir()):
        project = Project(**json.loads(project_path.read_text()))
        project_name = project.name
        for community_algo, community_files in project.communities.items():  # Iterating through community algorithms
            for file_id, file_data in project.files.items():
                if file_data.annotation:
                    distribution = file_data.annotation.distribution
                    argmax_dist = np.argmax(distribution)
                else:
                    argmax_dist = None

                file_node_id = None
                for x in project.dep_graph.nodes:
                    if project.dep_graph.nodes[x]['filePathRelative'] == file_id:
                        file_node_id = x
                        break

                community = None
                arcan_package = None
                graph = project.dep_graph.to_graph()
                if file_node_id:
                    community = community_files[str(file_node_id)]

                    arcan_package = [
                        neighbor for neighbor in graph.neighbors(file_node_id)
                        if graph[file_node_id][neighbor].get('labelE') == 'belongsTo'
                    ]

                assert len(arcan_package) <= 1

                rows.append({
                    'Project': project_name,
                    'File': file_data.path,
                    'AutoFL Package': file_data.package,
                    'Arcan Package': arcan_package[0] if arcan_package else None,
                    'argmax(Distribution)': argmax_dist,
                    'Unannotated': file_data.annotation.unannotated,
                    'Community Algo': community_algo,
                    'Community': community
                })

    # Creating the DataFrame
    # Creating the DataFrame
    df = pd.DataFrame(rows)

    # Displaying the DataFrame
    df.to_csv("../../data/aggregated/projects_stats.csv", index=False)