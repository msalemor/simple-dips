from agents.ai_agent_base import AIAgentBase
from services.azure_openai_service import AzureOpenAIService


class ChineseTranslationAgent(AIAgentBase):
    def __init__(self, llm: AzureOpenAIService = None):
        super().__init__(name="Chinese Translation Agent", llm=llm)
        self.system_prompt = "You are a translation agent. Translate the text as requested by the user from English to Chinese."
