from langgraph.graph import StateGraph, END

from app.agent_graph.state_schema import AgentState

from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.repo_structure_agent import RepoStructureAgent


def build_graph():

    workflow = StateGraph(AgentState)

    coordinator = CoordinatorAgent()
    structure_agent = RepoStructureAgent()

    # define nodes
    workflow.add_node("coordinator", coordinator.run)
    workflow.add_node("structure", structure_agent.run)

    # define flow
    workflow.set_entry_point("coordinator")

    workflow.add_edge("coordinator", "structure")
    workflow.add_edge("structure", END)

    return workflow.compile()