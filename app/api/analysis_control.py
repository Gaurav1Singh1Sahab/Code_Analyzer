from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from threading import Thread

from app.db.database import get_db
from app.services.state_service import create_analysis_state
from app.services.analysis_executor import run_analysis
from app.db.models import AnalysisState


router = APIRouter()

@router.post("/start-analysis")
def start_analysis(project_path: str, db: Session = Depends(get_db)):

    initial_state = {
        "project_path": project_path,
        "current_step": 0,
        "status": "running",

        "enabled_agents": ["structure", "api", "security", "best_practices", "sde", "pm"],

        "repo_structure": [],
        "api_endpoints": [],
        "security_issues": [],
        "best_practices": [],
        "sde_documentation": "",
        "pm_summary": ""
    }

    new_state = create_analysis_state(db, project_id=1, initial_state=initial_state)

    # 🔥 run in background
    Thread(target=run_analysis, args=(new_state.id,)).start()

    return {
        "analysis_id": new_state.id,
        "message": "Analysis started"
    }

@router.post("/pause/{analysis_id}")
def pause_analysis(analysis_id: int, db: Session = Depends(get_db)):

    db_state = db.query().filter(
        AnalysisState.id == analysis_id
    ).first()

    if not db_state:
        return {"error": "Analysis not found"}

    db_state.status = "paused"
    db.commit()

    return {"message": "Analysis paused"}



@router.post("/resume/{analysis_id}")
def resume_analysis(analysis_id: int, db: Session = Depends(get_db)):

    db_state = db.query(AnalysisState).filter(
        AnalysisState.id == analysis_id
    ).first()

    if not db_state:
        return {"error": "Analysis not found"}

    db_state.status = "running"
    db.commit()

    # 🔥 restart background execution
    Thread(target=run_analysis, args=(analysis_id,)).start()

    return {"message": "Analysis resumed"}