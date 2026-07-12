from pathlib import Path
from typing import Any

import faiss
import numpy as np
from numpy.typing import NDArray

from src.rag.document_loader import DocumentLoader
from src.rag.embedding_service import EmbeddingService


class FAISSIndex:
    """Manage the FAISS vector index."""

    INDEX_PATH = Path(__file__).resolve().parent.parent.parent / "knowledge" / "knowledge.index"

    def __init__(self) -> None:
        self.index: Any | None = None
        self.documents: list[dict[str, str]] = []

    def exists(self) -> bool:
        """
        Check whether the FAISS index exists and is up to date.
        """

        if not self.INDEX_PATH.exists():
            return False

        index_time = self.INDEX_PATH.stat().st_mtime

        for file in DocumentLoader.KNOWLEDGE_PATH.glob("*.md"):
            if file.stat().st_mtime > index_time:
                return False

        return True

    def build(self) -> None:
        """Build a new FAISS index from the knowledge documents."""

        self.documents = DocumentLoader.load_documents()

        texts = [doc["text"] for doc in self.documents]

        embeddings = EmbeddingService.encode_many(texts)

        vectors = np.array(embeddings, dtype="float32")

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

        faiss.write_index(self.index, str(self.INDEX_PATH))

    def load(self) -> None:
        """Load an existing FAISS index."""

        self.documents = DocumentLoader.load_documents()

        self.index = faiss.read_index(str(self.INDEX_PATH))

    def search(
        self,
        query: str,
        doc_type: str,
        top_k: int = 3,
    ) -> str:
        """
        Retrieve the most relevant documents.

        Returns:
            A concatenated string containing the retrieved context.
        """

        if self.index is None:
            raise RuntimeError("FAISS index has not been loaded.")

        query_embedding = EmbeddingService.encode(query)

        query_vector: NDArray[np.float32] = np.array([query_embedding], dtype="float32")

        _, indices = self.index.search(query_vector, len(self.documents))

        results: list[str] = []

        for idx in indices[0]:

            if idx == -1:
                continue

            document: dict[str, str] = self.documents[int(idx)]

            if document["doc_type"] != doc_type:
                continue

            results.append(document["text"])

            if len(results) >= top_k:
                break

        return "\n\n".join(results)
    