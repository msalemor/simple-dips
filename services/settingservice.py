import os
from dotenv import load_dotenv


class Settings:
    def __init__(self, dotenv_path=None):
        load_dotenv(dotenv_path)
        self._endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self._api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self._version = os.getenv("AZURE_OPENAI_VERSION")
        self._model = os.getenv("AZURE_OPENAI_MODEL")

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def api_key(self):
        return self._api_key

    @property
    def version(self):
        return self._version

    @property
    def model(self):
        return self._model


instance = None


def settings_instance():
    global instance
    if instance is None:
        instance = Settings()
    return instance
