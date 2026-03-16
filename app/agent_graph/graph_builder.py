from langgraph.graph import StateGraph, END

from app.agent_graph.state_schema import AgentState

from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.repo_structure_agent import RepoStructureAgent

from app.agents.api_signature_agent import APISignatureAgent


def build_graph():

    workflow = StateGraph(AgentState)

    coordinator = CoordinatorAgent()
    structure_agent = RepoStructureAgent()
    api_agent = APISignatureAgent()

    # define nodes
    workflow.add_node("coordinator", coordinator.run)
    workflow.add_node("structure", structure_agent.run)
    workflow.add_node("api_agent", api_agent.run)

    # define flow
    workflow.set_entry_point("coordinator")

    workflow.add_edge("coordinator", "structure")
    workflow.add_edge("structure", "api_agent")
    workflow.add_edge("api_agent", END)

    return workflow.compile()