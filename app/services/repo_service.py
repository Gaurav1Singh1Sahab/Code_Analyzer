import os
import zipfile
import subprocess
from app.core.config import settings


def clone_github_repo(repo_url: str, project_id: int):

    repo_path = os.path.join(settings.UPLOAD_DIR, f"project_{project_id}")

    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    subprocess.run(
        ["git", "clone", repo_url, repo_path],
        check=True
    )

    return repo_path


def extract_zip(zip_path: str, project_id: int):

    extract_path = os.path.join(settings.UPLOAD_DIR, f"project_{project_id}")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path