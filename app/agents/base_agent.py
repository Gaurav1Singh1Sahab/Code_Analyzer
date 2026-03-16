class BaseAgent:

    name = "BaseAgent"

    def run(self, state: dict) -> dict:
        """
        Each agent receives shared state
        and returns updated state
        """
        raise NotImplementedError