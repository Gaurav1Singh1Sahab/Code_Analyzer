from langgraph.graph import StateGraph, END

from app.agent_graph.state_schema import AgentState

from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.repo_structure_agent import RepoStructureAgent

from app.agents.api_signature_agent import APISignatureAgent

from app.agents.security_agent import SecurityAgent

from app.agents.best_practices_agent import BestPracticesAgent

from app.agents.sde_documentation_agent import SDEDocumentationAgent
from app.agents.pm_documentation_agent import PMDocumentationAgent


def build_graph():

    workflow = StateGraph(AgentState)

    coordinator = CoordinatorAgent()
    structure_agent = RepoStructureAgent()
    api_agent = APISignatureAgent()
    security_agent = SecurityAgent()
    best_practices_agent = BestPracticesAgent()
    sde_agent = SDEDocumentationAgent()
    pm_agent = PMDocumentationAgent()

    # define nodes
    workflow.add_node("coordinator", coordinator.run)
    workflow.add_node("structure", structure_agent.run)
    workflow.add_node("api_agent", api_agent.run)
    workflow.add_node("security_agent", security_agent.run)
    workflow.add_node("best_practices_agent", best_practices_agent.run)
    workflow.add_node("sde_agent", sde_agent.run)
    workflow.add_node("pm_agent", pm_agent.run)

    # define flow
    workflow.set_entry_point("coordinator")

    workflow.add_edge("coordinator", "structure")
    workflow.add_edge("structure", "api_agent")
    workflow.add_edge("api_agent", "security_agent")
    workflow.add_edge("security_agent", "best_practices_agent")
    workflow.add_edge("best_practices_agent", "sde_agent")
    workflow.add_edge("sde_agent", "pm_agent")
    workflow.add_edge("pm_agent", END)

    return workflow.compile()