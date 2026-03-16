import os
import re

from app.agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):

    name = "SecurityAgent"

    SECRET_PATTERN = re.compile(
        r"(password\s*=|secret\s*=|api_key\s*=|token\s*=)",
        re.IGNORECASE
    )

    SQL_PATTERN = re.compile(
        r"SELECT .* \+",
        re.IGNORECASE
    )

    DEBUG_PATTERN = re.compile(
        r"debug\s*=\s*True",
        re.IGNORECASE
    )

    def run(self, state: dict) -> dict:

        project_path = state["project_path"]

        print("SecurityAgent: scanning for security issues")

        issues = []

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

                if self.SECRET_PATTERN.search(code):
                    issues.append(f"Possible hardcoded secret in {file_path}")

                if self.SQL_PATTERN.search(code):
                    issues.append(f"Possible unsafe SQL query in {file_path}")

                if self.DEBUG_PATTERN.search(code):
                    issues.append(f"Debug mode enabled in {file_path}")

        print(f"Detected {len(issues)} security issues")

        state["security_issues"] = issues

        return state