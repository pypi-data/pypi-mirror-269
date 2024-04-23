import json
import pathlib
from typing import Literal, Optional, Union

from lango_cli_beta.constants import (
    BASE_JSON_SCHEMA,
    CLI_INVOKE_NAME,
    DEFAULT_CONFIG_PATH,
    INDEX_PATH_SCHEMA_LIST,
)

"""Configuration for the LangChain MongoDB RAG CLI."""


class RagConfig:
    llm: Literal[
        "claude_3_opus",
        "gpt_4_turbo",
        "command_r",
        "mistral_large",
        "gemini_pro",
        "fireworks_mixtral_8x7b",
    ]

    rag_type: Literal["basic", "query_construction"]

    ingest_path: str = None

    metadata: Union[dict, None] = None
    """Metadata to be applied to all documents in the vector store."""

    json_schema: Union[dict, None] = None
    """JSONSchema used for query construction. Required for query_construction rag_type."""

    chunk_size: int = 500

    chunk_overlap: int = 75

    def __init__(
        self,
        path_or_config: Optional[Union[str, dict]] = None,
    ) -> None:
        config_dict = {}
        # Check if a JSON file exists at DEFAULT_CONFIG_PATH, if it does, load it
        config_already_exists = pathlib.Path(DEFAULT_CONFIG_PATH).exists()
        if config_already_exists:
            with open(DEFAULT_CONFIG_PATH, "r") as f:
                config_dict = json.load(f)
        else:
            raise FileNotFoundError(
                f"""No config file found. Please run "{CLI_INVOKE_NAME} init <project name>" to create a new config file, then navigate into the project directory."""
            )

        if isinstance(path_or_config, str):
            # Read the config from a file
            with open(path_or_config, "r") as f:
                config_dict.update(json.load(f))
        elif isinstance(path_or_config, dict):
            config_dict.update(path_or_config)
        elif isinstance(path_or_config, pathlib.Path):
            with open(path_or_config, "r") as f:
                config_dict.update(json.load(f))
        else:
            raise ValueError(
                f"Either a file path or a config dictionary must be provided. Received: {type(path_or_config)}"
            )

        self.rag_type = config_dict["rag_type"]
        self.llm = config_dict["llm"]
        self.ingest_path = config_dict.get("ingest_path", None)
        self.metadata = config_dict.get("metadata", None)
        self.chunk_size = int(config_dict.get("chunk_size", 500))
        self.chunk_overlap = int(config_dict.get("chunk_overlap", 75))
        self.json_schema = config_dict.get("json_schema", None)

    def _ensure_path_index_in_schema(self, json_schema: Union[dict, None]) -> dict:
        """Ensure JSONSchema always contains an '_index' and '_path' field."""
        if json_schema is None:
            return BASE_JSON_SCHEMA
        else:
            # Check if propeties contains "_index" and "_path"
            # If it does, return, if it doesnt, add them via the INDEX_PATH_SCHEMA_DICT var
            if "_index" not in json_schema["properties"]:
                json_schema["properties"]["_index"] = INDEX_PATH_SCHEMA_LIST["_index"]
            if "_path" not in json_schema["properties"]:
                json_schema["properties"]["_path"] = INDEX_PATH_SCHEMA_LIST["_path"]
            return json_schema

    def save_config(self, config_path: str) -> None:
        """Write the config to a file."""
        with open(config_path, "w") as f:
            f.write(
                json.dumps(
                    {
                        "rag_type": self.rag_type,
                        "llm": self.llm,
                        "ingest_path": self.ingest_path,
                        "metadata": self.metadata,
                        "chunk_overlap": self.chunk_overlap,
                        "chunk_size": self.chunk_size,
                        "json_schema": self._ensure_path_index_in_schema(
                            self.json_schema
                        ),
                    }
                )
            )
