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





def run_analysis(state: dict):

    print("Starting step-based analysis...")

    while state.get("status") == "running":

        state = run_next_step(state)

        # simulate step delay (important for testing pause later)
        time.sleep(2)

        if state.get("status") == "completed":
            break

    return state