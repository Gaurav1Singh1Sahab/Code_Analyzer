from app.agents.base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):

    name = "CoordinatorAgent"

    def run(self, state: dict) -> dict:

        print("Coordinator: Starting analysis")

        # Validate configuration
        if "analysis_depth" not in state:
            state["analysis_depth"] = "standard"

        if "verbosity" not in state:
            state["verbosity"] = "medium"

        print(f"Analysis depth: {state['analysis_depth']}")
        print(f"Verbosity level: {state['verbosity']}")

        return state