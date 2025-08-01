import os
import requests
from typing import List
from langchain_core.embeddings import Embeddings

class EuriaiEmbeddings(Embeddings):
    """Euriai API embeddings for LangChain."""
    
    def __init__(self, model: str = "text-embedding-3-small"):
        self.api_key = os.environ.get("EURIAI_API_KEY")
        if not self.api_key:
            raise ValueError("EURIAI_API_KEY not found in .env file")
        self.model = model

    def _embed(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        try:
            response = requests.post(
                "https://api.euron.one/api/v1/euri/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"input": text, "model": self.model}
            )
            response.raise_for_status()
            return response.json()['data'][0]['embedding']
        except Exception as e:
            print(f"Embedding API error: {e}")
            return []

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents."""
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a query."""
        return self._embed(text)
