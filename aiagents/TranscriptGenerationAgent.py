from aiagents.AIAgentBase import AIAgentBase
from services.azureopenaiservice import AzureOpenAIService


class TranscriptGenerationAgent(AIAgentBase):
    def __init__(self, llm: AzureOpenAIService = None):
        super().__init__(name="TranscriptGenerationAgent", llm=llm)
        self.system_prompt = "You are a transcription generation agent. Generate a transcription as requested by the user."
