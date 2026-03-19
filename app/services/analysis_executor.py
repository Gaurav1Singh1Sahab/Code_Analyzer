
from app.services.state_service import update_analysis_state, get_analysis_state
from app.db.database import SessionLocal
import time

from app.agents.repo_structure_agent import RepoStructureAgent
from app.agents.api_signature_agent import APISignatureAgent
from app.agents.security_agent import SecurityAgent
from app.agents.best_practices_agent import BestPracticesAgent
from app.agents.sde_documentation_agent import SDEDocumentationAgent
from app.agents.pm_documentation_agent import PMDocumentationAgent


AGENT_FLOW = [
    ("structure", RepoStructureAgent()),
    ("api", APISignatureAgent()),
    ("security", SecurityAgent()),
    ("best_practices", BestPracticesAgent()),
    ("sde", SDEDocumentationAgent()),
    ("pm", PMDocumentationAgent()),
]

def run_next_step(state: dict):

    current_step = state.get("current_step", 0)

    # ✅ If all steps done
    if current_step >= len(AGENT_FLOW):
        state["status"] = "completed"
        print("Analysis completed")
        return state

    agent_name, agent = AGENT_FLOW[current_step]

    print(f"Running step {current_step}: {agent_name}")

    # run agent
    state = agent.run(state)

    # move to next step
    state["current_step"] = current_step + 1

    return state





def run_analysis(analysis_id: int):

    db = SessionLocal()

    print(f"Starting analysis for ID: {analysis_id}")

    while True:

        # 🔥 always fetch latest state from DB
        db_state = get_analysis_state(db, analysis_id)

        if not db_state:
            print("Analysis state not found")
            break

        state = db_state.state_data

        # ✅ Stop if paused
        if db_state.status == "paused":
            print("Analysis paused")
            break

        # ✅ Stop if completed
        if db_state.status == "completed":
            print("Analysis already completed")
            break

        # 👉 run next step
        state = run_next_step(state)

        # ✅ update status if finished
        if state.get("status") == "completed":
            db_state.status = "completed"

        # 🔥 save state after each step
        update_analysis_state(db, analysis_id, state)

        time.sleep(2)

    db.close()