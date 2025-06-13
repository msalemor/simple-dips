from aiagents.AIAgentBase import AIAgentBase
from services.azureopenaiservice import AzureOpenAIService


class ChineseTranslationAgent(AIAgentBase):
    def __init__(self, llm: AzureOpenAIService = None):
        super().__init__(name="TranscriptGenerationAgent", llm=llm)
        self.system_prompt = "You are a translation agent. Translate the text as requested by the user from English to Chinese."
