from typing import Any, cast

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Service responsible for generating text embeddings."""

    _model: SentenceTransformer | None = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """Return a singleton instance of the embedding model."""
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    @classmethod
    def encode(cls, text: str) -> list[float]:
        """Generate an embedding for a single text."""
        model = cls.get_model()
        raw_embedding: Any = cast(Any, model).encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        embedding = cast(np.ndarray, raw_embedding)
        return cast(list[float], cast(Any, embedding).tolist())

    @classmethod
    def encode_many(cls, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        model = cls.get_model()
        raw_embeddings: Any = cast(Any, model).encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        embeddings = cast(np.ndarray, raw_embeddings)
        return cast(list[list[float]], cast(Any, embeddings).tolist())
