from src.rag.faiss_index import FAISSIndex


class RAGManager:
    """Facade for retrieving contextual information from the knowledge base."""

    _index = FAISSIndex()

    @classmethod
    def initialize(cls) -> None:
        """Build or load the FAISS index."""

        if cls._index.exists():
            cls._index.load()
        else:
            cls._index.build()
            cls._index.load()

    @classmethod
    def retrieve(
        cls,
        query: str,
        doc_type: str,
        top_k: int = 3,
    ) -> str:
        """
        Retrieve the most relevant context for a query.

        Args:
            query: User query.
            doc_type: Either "story" or "task".
            top_k: Number of retrieved documents.

        Returns:
            Concatenated context.
        """

        return cls._index.search(
            query=query,
            doc_type=doc_type,
            top_k=top_k,
        )
    