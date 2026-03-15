import os
import time

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.repo_service import clone_github_repo
from app.services.code_ingestion_service import ingest_repository


def run_analysis(project_id: int, repo_url: str = None):

    db: Session = SessionLocal()

    print(f"Starting analysis for project {project_id}")

    repo_path = None

    if repo_url:
        repo_path = clone_github_repo(repo_url, project_id)

    if repo_path:
        ingest_repository(repo_path, project_id, db)

    time.sleep(2)

    print(f"Analysis completed for project {project_id}")