from openai import OpenAI
from app.agents.base_agent import BaseAgent


class PMDocumentationAgent(BaseAgent):

    name = "PMDocumentationAgent"

    def run(self, state: dict) -> dict:

        def run(self, state: dict) -> dict:

            if "pm" not in state["enabled_agents"]:
                print("PMDocumentationAgent: skipped")
                return state

        print("PMDocumentationAgent: generating product summary")

        client = OpenAI()

        api_data = state.get("api_endpoints", [])

        prompt = f"""
You are a product manager.

Explain this project in simple business terms.

API Endpoints:
{api_data}

Generate:
1. What this product does
2. Key features
3. User journey
4. Business value

Keep it non-technical and easy to understand.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert product manager."},
                {"role": "user", "content": prompt}
            ]
        )

        state["pm_summary"] = response.choices[0].message.content

        print("PMDocumentationAgent: completed")

        return state