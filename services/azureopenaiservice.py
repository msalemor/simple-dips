from openai import AzureOpenAI
from typing import List, Dict, Optional
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from services.settingservice import Settings, settings_instance


class AzureOpenAIService:
    def __init__(self, settings: Settings = None):
        self._settings = settings or settings_instance()
        if self._settings.api_key is None:
            token_provider = get_bearer_token_provider(
                DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
            )
            self.client = AzureOpenAI(
                azure_endpoint=self._settings.endpoint,
                credential=token_provider,
                api_version=self._settings.version,
            )
        else:
            self.client = AzureOpenAI(
                azure_endpoint=self._settings.endpoint,
                api_key=self._settings.api_key,
                api_version=self._settings.version,
            )
        self.deployment_name = self._settings.model

    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """
        Get a chat completion from Azure OpenAI.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            temperature: Controls randomness (0-2)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters for the API

        Returns:
            The assistant's response as a string
        """
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return response.choices[0].message.content
