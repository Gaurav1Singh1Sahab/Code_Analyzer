from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.agent_graph.graph_builder import build_graph

router = APIRouter()


class AnalysisRequest(BaseModel):
    project_path: str
    analysis_depth: str = "standard"
    verbosity: str = "medium"
    enabled_agents: List[str] = [
        "structure",
        "api",
        "security",
        "best_practices",
        "sde",
        "pm"
    ]


@router.post("/analyze-agents")
def run_agent_analysis(request: AnalysisRequest):

    graph = build_graph()

    initial_state = {

        "project_id": 0,
        "project_path": request.project_path,

        "analysis_depth": request.analysis_depth,
        "verbosity": request.verbosity,
        "enabled_agents": request.enabled_agents,

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