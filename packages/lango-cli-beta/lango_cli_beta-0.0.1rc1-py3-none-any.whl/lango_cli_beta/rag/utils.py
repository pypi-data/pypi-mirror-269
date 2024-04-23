from typing import List

from langchain_core.documents import Document


def _get_llm(llm: str):
    match llm:
        case "claude_3_opus":
            from langchain_anthropic.chat_models import ChatAnthropic

            return ChatAnthropic(model_name="claude-3-opus-20240229", temperature=0)
        case "gpt_4_turbo":
            from langchain_openai.chat_models import ChatOpenAI

            return ChatOpenAI(model="gpt-4-turbo", temperature=0)
        case "command_r":
            from langchain_cohere.chat_models import ChatCohere

            return ChatCohere(model="command-r", temperature=0)
        case "mistral_large":
            from langchain_mistralai.chat_models import ChatMistralAI

            return ChatMistralAI(model="mistral-large-latest", temperature=0)
        case "gemini_pro":
            from langchain_google_vertexai.chat_models import ChatVertexAI

            return ChatVertexAI(model_name="gemini-pro", temperature=0)
        case "fireworks_mixtral_8x7b":
            from langchain_fireworks.chat_models import ChatFireworks

            return ChatFireworks(
                model="accounts/fireworks/models/mixtral-8x7b-instruct", temperature=0
            )
        case _:
            raise ValueError(f"Invalid LLM received: {llm}.")


def _clean_mongo_docs(docs: List[Document]) -> List[Document]:
    """Remove the _id field from a list of documents."""
    cleaned_documents = []
    for doc in docs:
        if doc is not None:
            if "_id" in doc.metadata:
                del doc.metadata["_id"]
            cleaned_documents.append(doc)
    return cleaned_documents
