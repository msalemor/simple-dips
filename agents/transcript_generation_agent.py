from agents.agent_base import AgentBase
from services.azure_openai_service import AzureOpenAIService


class TranscriptGenerationAgent(AgentBase):
    def __init__(self, llm: AzureOpenAIService = None):
        super().__init__(name="Transcript Generation Agent", llm=llm)
        self.system_prompt = "You are a transcription generation agent. Generate a transcription as requested by the user."
