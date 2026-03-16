from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    # project info
    project_id: int
    project_path: str

    # analysis configuration
    analysis_depth: str
    verbosity: str

    # extracted information
    repo_structure: Dict[str, Any]
    api_endpoints: List[Dict[str, Any]]

    # agent findings
    security_issues: List[str]
    best_practices: List[str]

    # generated outputs
    architecture_summary: str
    sde_documentation: str
    pm_summary: str