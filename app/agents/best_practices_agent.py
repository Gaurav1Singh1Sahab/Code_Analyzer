# from duckduckgo_search import DDGS

from ddgs import DDGS

from app.agents.base_agent import BaseAgent


class BestPracticesAgent(BaseAgent):

    name = "BestPracticesAgent"

    def search_web(self, query):

        results = []

        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=3):
                    results.append(r["title"])
        except:
            pass

        return results

    def run(self, state: dict) -> dict:

        print("BestPracticesAgent: researching framework best practices")

        best_practices = []

        # FastAPI research
        fastapi_results = self.search_web(
            "FastAPI async endpoint best practices"
        )

        best_practices.append({
            "topic": "FastAPI Best Practices",
            "results": fastapi_results
        })

        # SQLAlchemy research
        sqlalchemy_results = self.search_web(
            "SQLAlchemy session management best practices"
        )

        best_practices.append({
            "topic": "SQLAlchemy Best Practices",
            "results": sqlalchemy_results
        })

        # OWASP research
        owasp_results = self.search_web(
            "OWASP authentication security recommendations"
        )

        best_practices.append({
            "topic": "OWASP Security",
            "results": owasp_results
        })

        print("BestPracticesAgent: research completed")

        state["best_practices"] = best_practices

        return state