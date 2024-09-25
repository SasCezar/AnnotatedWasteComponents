import json
from pathlib import Path
import pandas as pd
from stats.simple import SimpleStats

if __name__ == '__main__':
    projects_dir = Path("/WasteComponents/data/annotated")
    df = []
    for project_path in projects_dir.iterdir():
        project = json.load(project_path.open())
        p_name = project_path.stem
        p_stats = SimpleStats.stats(project)
        p_stats["project"] = p_name
        df.append(p_stats)

    df = pd.DataFrame(df)
    df.to_csv('simple_stats.csv', index=False)
