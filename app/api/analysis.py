from fastapi import APIRouter
from app.agent_graph.graph_builder import build_graph

router = APIRouter()


@router.post("/analyze-agents")
def run_agent_analysis(project_path: str):

    graph = build_graph()

    initial_state = {

        "project_id": 0,
        "project_path": project_path,

        "analysis_depth": "standard",
        "verbosity": "medium",

        "repo_structure": [],
        "api_endpoints": [],

        "security_issues": [],
        "best_practices": [],

        "architecture_summary": "",
        "sde_documentation": "",
        "pm_summary": ""
    }

    result = graph.invoke(initial_state)

    return result