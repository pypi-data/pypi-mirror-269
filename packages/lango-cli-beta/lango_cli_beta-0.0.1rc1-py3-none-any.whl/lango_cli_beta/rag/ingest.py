"""
Logic for ingesting documents into MongoDB vector store
"""

import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich import print as rich_print

from lango_cli_beta.rag_config import RagConfig
from lango_cli_beta.utils import initialize_vectorstore


def _read_file_or_folder(path: str) -> List[dict]:
    """Reads a list of dictionaries containing the file path,
    and text the file contains."""

    if os.path.isfile(path):
        with open(path, "r") as f:
            return [{"path": path, "text": f.read()}]
    elif os.path.isdir(path):
        data = []
        for file in os.listdir(path):
            if file.endswith(".txt"):
                joined_path = os.path.join(path, file)
                with open(joined_path, "r") as f:
                    data.append({"path": joined_path, "text": f.read()})
        return data


def _construct_metadata(
    metadata: Optional[dict] = None,
    index: int = None,
    path: str = None,
    split_texts: List[str] = None,
):
    """Create a metadata list for each split text, containing any metadata provided
    and the index of the split text."""

    metadata_list: List[dict] = []
    for i, _ in enumerate(split_texts):
        if metadata is None:
            metadata_dict = {"_index": i, "_path": path}
        else:
            metadata_dict = {**metadata, "_index": i, "_path": path}
        metadata_list.append(metadata_dict)

    return metadata_list


def _transform_data_to_documents(
    ingest_path: str,
    metadata: Optional[dict] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 75,
) -> dict:
    """
    Convert the data provided by the user, into a list
    of LangChain documents.
    """
    # Read the data from the ingest path
    data = _read_file_or_folder(ingest_path)

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=int(chunk_size),
        chunk_overlap=int(chunk_overlap),
        length_function=len,
        is_separator_regex=False,
    )

    docs: List[Document] = []

    unique_metadata_keys = set()

    for i, item in enumerate(data):
        text = item["text"]
        path = item["path"]

        split_texts = text_splitter.split_text(text)
        metadata_list = _construct_metadata(
            metadata=metadata, index=i, path=path, split_texts=split_texts
        )

        # Update the unique metadata keys with the keys from the metadata.
        for metadata_dict in metadata_list:
            unique_metadata_keys.update(metadata_dict.keys())

        docs = docs + text_splitter.create_documents(
            split_texts, metadatas=metadata_list
        )

    return {
        "docs": docs,
        "unique_metadata_keys": unique_metadata_keys,
    }


class Ingester:
    ingest_path: str

    metadata: Optional[dict] = None

    chunk_size: int = 500

    chunk_overlap: int = 75

    should_ingest: bool = True

    def __init__(self, config: RagConfig) -> None:
        if config.ingest_path is None:
            raise ValueError("An ingest path must be provided when ingesting data.")

        self.ingest_path = config.ingest_path
        self.metadata = config.metadata
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap
        # Env var which controls whether or not to ingest data.
        # Defaults to True, and will only be False if explicitly set to "False".
        self.should_ingest = os.getenv("SHOULD_INGEST_DATA") != "False"

    def ingest_data(self) -> None:
        """Ingest the data into the MongoDB vector store.
        First, convert the raw ingest data into LangChain documents.
        Then, ingest the documents into the MongoDB vector store
        using the MongoDocumentStore to index the documents.
        """
        docs_and_metadata_keys = _transform_data_to_documents(
            self.ingest_path,
            metadata=self.metadata,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        docs = docs_and_metadata_keys["docs"]
        vectorstore = initialize_vectorstore()

        ids = []
        if self.should_ingest:
            ids = vectorstore.add_documents(docs)

        rich_print(f"Added [bold #0af2b0]{len(ids)}[/bold #0af2b0] docs.")
