import os
import re

from app.agents.base_agent import BaseAgent


class APISignatureAgent(BaseAgent):

    name = "APISignatureAgent"

    ROUTE_PATTERN = re.compile(
        r"@router\.(get|post|put|delete|patch)\(\"([^\"]+)\"\)"
    )

    FUNCTION_PATTERN = re.compile(
        r"def\s+([a-zA-Z0-9_]+)\("
    )

    def run(self, state: dict) -> dict:

        project_path = state["project_path"]

        print("APISignatureAgent: scanning for API endpoints")

        endpoints = []

        for root, dirs, files in os.walk(project_path):

            for file in files:

                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                except:
                    continue

                routes = self.ROUTE_PATTERN.findall(code)

                if not routes:
                    continue

                functions = self.FUNCTION_PATTERN.findall(code)

                for i, route in enumerate(routes):

                    method, path = route

                    function_name = (
                        functions[i] if i < len(functions) else "unknown"
                    )

                    endpoints.append({
                        "method": method.upper(),
                        "path": path,
                        "function": function_name,
                        "file": file_path
                    })

        print(f"Detected {len(endpoints)} API endpoints")

        state["api_endpoints"] = endpoints

        return state