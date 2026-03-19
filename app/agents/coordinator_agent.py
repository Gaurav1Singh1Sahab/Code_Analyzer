from app.agents.base_agent import BaseAgent


class CoordinatorAgent(BaseAgent):

    name = "CoordinatorAgent"

    def run(self, state: dict) -> dict:

        print("Coordinator: Starting analysis")

        # defaults
        state.setdefault("analysis_depth", "standard")
        state.setdefault("verbosity", "medium")

        # 🔥 default enabled agents
        state.setdefault("enabled_agents", [
            "structure",
            "api",
            "security",
            "best_practices",
            "sde",
            "pm"
        ])

        print(f"Depth: {state['analysis_depth']}")
        print(f"Verbosity: {state['verbosity']}")
        print(f"Enabled Agents: {state['enabled_agents']}")

        return state