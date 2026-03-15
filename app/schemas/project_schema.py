from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):

    name: str
    description: Optional[str] = None
    github_url: Optional[str] = None