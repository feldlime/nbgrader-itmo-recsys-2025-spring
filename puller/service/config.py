from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    github_token: str
    target_dir: str
    students_tsv_path: Optional[str] = None
    jupyter_url: str
    
    class Config:
        env_file = ".env"
