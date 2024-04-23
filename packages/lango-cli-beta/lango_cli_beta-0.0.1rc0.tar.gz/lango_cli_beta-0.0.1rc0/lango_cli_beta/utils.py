import os

from langchain_cohere import CohereEmbeddings
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch


def initialize_vectorstore() -> MongoDBAtlasVectorSearch:
    """Initialize the MongoDB vector store."""
    MONGODB_URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("MONGODB_VECTORSTORE_NAME")
    COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")
    ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("MONGODB_VECTORSTORE_INDEX_NAME")

    vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
        MONGODB_URI,
        DB_NAME + "." + COLLECTION_NAME,
        CohereEmbeddings(model="embed-english-v3.0"),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )
    return vectorstore
