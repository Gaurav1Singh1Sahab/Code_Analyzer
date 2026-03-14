from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Project, User
from app.schemas.project_schema import ProjectCreate
from app.core.dependencies import get_current_user
from app.core.config import settings

from app.services.analyzer import run_analysis

import os
import shutil
import re

router = APIRouter()


# -----------------------------
# Create Project
# -----------------------------
@router.post("/projects")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "project_id": new_project.id,
        "message": "Project created successfully"
    }


# -----------------------------
# Add Repository (3 Options)
# -----------------------------
@router.post("/projects/{project_id}/repository")
def add_repository(
    project_id: int,
    github_url: str | None = Form(None),
    zip_file: UploadFile | None = File(None),
    code_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ---------- Check Project Exists ----------
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found. Please create a project first."
        )

    # ---------- Ensure Only One Input ----------
    inputs_provided = sum([
        bool(github_url),
        bool(zip_file),
        bool(code_file)
    ])

    if inputs_provided == 0:
        raise HTTPException(
            status_code=400,
            detail="Provide one input: GitHub URL, ZIP file, or single code file."
        )

    if inputs_provided > 1:
        raise HTTPException(
            status_code=400,
            detail="Provide ONLY one input method (GitHub URL OR ZIP OR code file)."
        )

    project_dir = os.path.join(settings.UPLOAD_DIR, str(project_id))
    os.makedirs(project_dir, exist_ok=True)

    # -----------------------------
    # GitHub Repository
    # -----------------------------
    if github_url:

        github_pattern = r"^https://github.com/.+/.+"

        if not re.match(github_pattern, github_url):
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub URL format."
            )

        return {
            "message": "GitHub repository registered successfully",
            "project_id": project_id,
            "github_url": github_url
        }

    # -----------------------------
    # ZIP Repository Upload
    # -----------------------------
    if zip_file:

        if not zip_file.filename.endswith(".zip"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only ZIP repositories are allowed."
            )

        file_path = os.path.join(project_dir, zip_file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(zip_file.file, buffer)

        return {
            "message": "ZIP repository uploaded successfully",
            "project_id": project_id,
            "file_name": zip_file.filename
        }

    # -----------------------------
    # Single Code File Upload
    # -----------------------------
    if code_file:

        allowed_extensions = [
            ".py", ".js", ".ts", ".java", ".cpp", ".go", ".rs"
        ]

        if not any(code_file.filename.endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Upload a valid source code file."
            )

        file_path = os.path.join(project_dir, code_file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(code_file.file, buffer)

        return {
            "message": "Single code file uploaded successfully",
            "project_id": project_id,
            "file_name": code_file.filename
        }


@router.post("/projects/{project_id}/analyze")
def start_analysis(
    project_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    background_tasks.add_task(run_analysis, project_id)

    return {
        "message": "Analysis started",
        "project_id": project_id,
        "status": "processing"
    }