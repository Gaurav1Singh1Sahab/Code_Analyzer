from openai import OpenAI
from app.agents.base_agent import BaseAgent


class SDEDocumentationAgent(BaseAgent):

    name = "SDEDocumentationAgent"

    def run(self, state: dict) -> dict:

        if "sde" not in state["enabled_agents"]:
            print("SDEDocumentationAgent: skipped")
            return state

        print("SDEDocumentationAgent: generating technical documentation")

        client = OpenAI()

        api_data = state.get("api_endpoints", [])
        security = state.get("security_issues", [])
        structure = state.get("repo_structure", [])

        prompt = f"""
You are a senior software engineer.

Generate technical documentation for this project:

Project Structure:
{structure}

API Endpoints:
{api_data}

Security Issues:
{security}

Include:
1. Architecture overview
2. API documentation
3. Security observations
4. Suggestions for improvement

Keep it clear and structured.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert software architect."},
                {"role": "user", "content": prompt}
            ]
        )

        state["sde_documentation"] = response.choices[0].message.content

        print("SDEDocumentationAgent: completed")

        return state