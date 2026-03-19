from sqlalchemy.orm import Session
from app.db.models import AnalysisState


def create_analysis_state(db: Session, project_id: int, initial_state: dict):

    new_state = AnalysisState(
        project_id=project_id,
        status="running",
        current_step=0,
        state_data=initial_state,
        user_context=[]
    )

    db.add(new_state)
    db.commit()
    db.refresh(new_state)

    return new_state


def get_analysis_state(db: Session, analysis_id: int):

    return db.query(AnalysisState).filter(
        AnalysisState.id == analysis_id
    ).first()


def update_analysis_state(db: Session, analysis_id: int, state: dict):

    db_state = get_analysis_state(db, analysis_id)

    if not db_state:
        return None

    db_state.state_data = state
    db_state.current_step = state.get("current_step", 0)
    db_state.status = state.get("status", "running")

    db.commit()
    db.refresh(db_state)

    return db_state