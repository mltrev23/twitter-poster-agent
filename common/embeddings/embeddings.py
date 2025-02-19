from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from typing import Optional

class EmbeddingProvider:

    def __init__(self, embedding_provider, model_name: Optional[str] = None):
        self._model_name = model_name
        match embedding_provider:
            case "sentence-transformer":
                if not model_name:
                    self._model_name = "BAAI/bge-multilingual-gemma2"
                self._embeddings = HuggingFaceEmbeddings(model_name=self._model_name)
            case "open-ai":
                if not model_name:
                    self._model_name = "text-embedding-3-large"
                self._embeddings = OpenAIEmbeddings(model=self._model_name)
            case "NVIDIA":
                if not model_name:
                    self._model_name = "NV-Embed-v2"
                self._embeddings = NVIDIAEmbeddings(model=self._model_name)

    @property
    def embeddings(self):
        return self._embeddings