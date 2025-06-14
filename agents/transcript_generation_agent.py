from agents.ai_agent_base import AIAgentBase
from services.azure_openai_service import AzureOpenAIService


class TranscriptGenerationAgent(AIAgentBase):
    def __init__(self, llm: AzureOpenAIService = None):
        super().__init__(name="Transcript Generation Agent", llm=llm)
        self.system_prompt = "You are a transcription generation agent. Generate a transcription as requested by the user."
