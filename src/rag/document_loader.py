from pathlib import Path


class DocumentLoader:
    """Loads knowledge documents from the project."""

    KNOWLEDGE_PATH = Path(__file__).resolve().parent.parent.parent / "knowledge"

    @classmethod
    def load_documents(cls) -> list[dict[str, str]]:
        """
        Load every Markdown document from the knowledge folder.

        Returns:
            A list of dictionaries with:
                - source
                - doc_type
                - text
        """

        documents: list[dict[str, str]] = []

        for file in sorted(cls.KNOWLEDGE_PATH.glob("*.md")):
            text = file.read_text(encoding="utf-8").strip()

            documents.append(
                {
                    "source": file.name,
                    "doc_type": cls._get_document_type(file.name),
                    "text": text,
                }
            )

        return documents

    @staticmethod
    def _get_document_type(filename: str) -> str:
        """Determine whether the document belongs to stories or tasks."""

        if filename.startswith(("07", "08")):
            return "task"

        return "story"
