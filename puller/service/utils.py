from pathlib import Path
from typing import Dict, List
import csv


REPO_COLUMN = 'Github repo'


def load_repositories_from_file(path: str) -> List[Dict]:
    """Load repositories from a file object"""
    try:
        content = Path(path).read_text().splitlines()
        repos = []
        reader = csv.DictReader(content, delimiter='\t')
        for row in reader:
            if REPO_COLUMN not in row or not row[REPO_COLUMN]:
                continue
            # Convert https://github.com/user/repo to user/repo format
            repo_url = row[REPO_COLUMN]
            repo = repo_url.removeprefix('https://github.com/')
            repos.append({'repository': repo})
        return repos
    except Exception as e:
        raise ValueError(f"Error loading repositories: {str(e)}")
