import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict
import os
import shutil

from github import Github
from github.ContentFile import ContentFile
from github.Auth import Token


class GitHubClient:
    def __init__(self, token: str):
        self.github = Github(auth=Token(token))
        self._pull_status: Dict[str, Dict] = {}

    def pull_homework(self, repo_name: str, homework_name: str, target_dir: str) -> dict:
        """Pull homework files from a specific branch and folder"""
        try:
            print("pull_homework")
            print("repo_name", repo_name)  
            repo = self.github.get_repo(repo_name)
            print("repo", repo)
            
            # Get contents from homework folder in the homework branch
            try:
                contents = repo.get_contents(f'notebooks/{homework_name}', ref=homework_name)
                print("contents", contents)
            except Exception as e:
                return {
                    'success': False,
                    'timestamp': datetime.now(),
                    'message': f'Homework folder or branch not found: {str(e)}'
                }
            
            # Download all files
            if isinstance(contents, ContentFile):
                contents = [contents]
                
            contents = [content for content in contents if content.name.endswith(('.py', '.ipynb'))]
            
            # Create target directory
            if contents:
                username = repo_name.split('/')[0]
                now_dt = datetime.now(tz=timezone.utc)
                target_folder_name = f"{username}+{homework_name}+{now_dt:%Y-%m-%dT%H:%M:%S} UTC+00"
                target_path = Path(target_dir) / target_folder_name
                target_path.mkdir(exist_ok=True, parents=True)
                
            for content in contents:
                print(f"{content.name=}", flush=True)
                print(f"{content.size=}", flush=True)
                target_file_path = target_path / content.name
                
                blob = repo.get_git_blob(content.sha)
                print(f"Blob is loaded, {blob.encoding=}")
                blob_content = blob.content
                if blob.encoding == "base64":
                    blob_content = base64.b64decode(blob_content).decode("utf-8")
                target_file_path.write_text(blob_content)
            
            status = {
                'success': True,
                'timestamp': datetime.now(),
                'message': f'Successfully pulled homework {homework_name} from {repo_name}'
            }
        except Exception as e:
            status = {
                'success': False,
                'timestamp': datetime.now(),
                'message': str(e)
            }
        
        self._pull_status[(repo_name, homework_name)] = status
        return status

    def get_pull_status(self, repo_name: str, homework_name: str) -> dict:
        """Get status of the last pull for a repository and homework"""
        return self._pull_status.get((repo_name, homework_name), {
            'success': None,
            'timestamp': None,
            'message': 'No pull attempts yet'
        })

    def pull_all_homeworks(self, repos: List[dict], homework_name: str, target_dir: str) -> Dict[str, dict]:
        """Pull homework from all repositories"""
        results = {}
        for repo in repos:
            results[repo['repository']] = self.pull_homework(
                repo['repository'],
                homework_name,
                target_dir
            )
        return results
