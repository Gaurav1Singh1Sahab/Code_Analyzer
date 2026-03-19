import os
from app.agents.base_agent import BaseAgent


class RepoStructureAgent(BaseAgent):

    name = "RepoStructureAgent"

    def run(self, state: dict) -> dict:

        if "structure" not in state["enabled_agents"]:
            print("RepoStructureAgent: skipped")
            return state
            
        project_path = state["project_path"]

        print(f"RepoStructureAgent: analyzing project structure at {project_path}")

        if not os.path.exists(project_path):
            print("Project path does not exist!")

        structure = []

        for root, dirs, files in os.walk(project_path):
            for d in dirs:
                structure.append(os.path.join(root, d))

        state["repo_structure"] = structure

        print(f"Detected {len(structure)} folders")

        return state