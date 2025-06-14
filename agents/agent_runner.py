from agents.agent_base import AgentBase
from services.log_service import get_logger

logger = get_logger(__name__)


class AgentRunner:
    def __init__(self, agents: list[AgentBase] | None = None):
        if not agents:
            raise ValueError("At least one agent must be provided")
        self.agents: list[AgentBase] = []

    def run(
        self, task: str, messages: list[dict[str, str]] | None = None
    ) -> list[dict[str, str]]:
        if not task:
            raise ValueError("Task must be provided")
        shared_state: list[dict[str, str]] = []

        if messages:
            shared_state = messages
        shared_state.append({"role": "user", "content": task})

        for agent in self.agents:
            logger.info(f"Activating agent: {agent.name}")
            res = agent.completion(
                messages=shared_state,
                temperature=0.1,
                shared_state=self.shared_state,
            )
            logger.info(f"Agent {agent.name} response:\n{res}")
            shared_state.append({"role": "user", "content": res})

        return shared_state
