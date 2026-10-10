from typing import Any

from sentence_transformers import SentenceTransformer

from mypkg.config import Settings

settings = Settings()


class TextEmbedder:
    def __init__(self) -> None:
        # Extract secret value safely if key exists
        api_token = settings.hf_token.get_secret_value() if settings.hf_token else None

        # Model downloads from HF Hub
        self.model = SentenceTransformer(
            model_name_or_path=settings.model_name, token=api_token
        )

    def get_embeddings(self, text: str | list[str]) -> Any:
        """Generates dense vector embeddings for input text."""
        return self.model.encode(text, convert_to_numpy=True).tolist()

    def predict(self, input_text: str) -> dict[Any, Any]:
        """
        Example predict function:
        Computes the embedding for the input text and returns its vector representation.
        """
        embedding = self.get_embeddings(input_text)

        result = {
            "text": input_text,
            "embedding_dim": len(embedding),
            "embedding": embedding,
        }

        return result
