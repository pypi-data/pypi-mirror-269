import os
from pathlib import Path

from langchain_core.messages import SystemMessage

SYSTEM_MESSAGE = SystemMessage(
    content="You are a helpful assistant.\n"
    + "Use any context provided to answer the users questions.\m"
    + "If you do not know an answer, say so. Do not make up information."
)


INDEX_PATH_SCHEMA_LIST = {
    "_index": {"type": "number", "description": "The index of the document chunk."},
    "_path": {"type": "string", "description": "The path to the original document."},
}

BASE_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "extract_filters_from_query",
    "description": "A tool to use for extracting filters from a given query.",
    "type": "object",
    "properties": INDEX_PATH_SCHEMA_LIST,
}

CLI_INVOKE_NAME = "lango-cli"

DEFAULT_RAG_CONFIG = {
    "rag_type": "basic",
    "llm": "anthropic",
    "chunk_size": 500,
    "chunk_overlap": 75,
    "metadata": {},
    "json_schema": BASE_JSON_SCHEMA,
}

DEFAULT_CONFIG_FILE_NAME = "lango_cli.config.json"

SAMPLE_DATA_FOLDER_NAME = "_sample_data"

DEFAULT_CONFIG_PATH = Path.cwd() / DEFAULT_CONFIG_FILE_NAME

JSON_SCHEMA_REQUIRED_MESSAGE = "JSONSchema is required for query construction. Please provide a valid JSON file path, or stringified JSON."

# Script to get the container's IP address and start the lango-cli server.
# This script is used in the Dockerfile for the `lango-cli export` command.
GET_IP_AND_START_SCRIPT = """
#!/bin/bash

# Get the container's IP address
CONTAINER_IP=$(hostname -i)

# Log the IP address and instructions
echo "Start the Docker container, then navigate to $CONTAINER_IP:8000/docs to visit the server"

# Start the lango-cli server
lango-cli start
"""

# Start script for the `lango-cli export` command.
# See the `GET_IP_AND_START_SCRIPT` constant for more information.
GET_IP_AND_START_FILE_NAME = "get_ip_and_start.sh"

# While the repo is still private, cloning will require authentication.
PIP_INSTALL_GIT_URI = os.getenv(
    "PIP_INSTALL_GIT_URI", "git+ssh://git@github.com/langchain-ai/mongo-rag-cli.git"
)

# Docker file for the `lango-cli export` command.
BASE_DOCKERFILE = f"""
# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the config file and the script into the container
COPY {DEFAULT_CONFIG_FILE_NAME} .
COPY {GET_IP_AND_START_FILE_NAME} .

# Make the script executable
RUN chmod +x {GET_IP_AND_START_FILE_NAME}

# Install git
RUN apt-get update && apt-get install -y git

# Install the Lango CLI
RUN pip install {PIP_INSTALL_GIT_URI}

# Set the default command to run when the container starts
CMD ["sh", "{GET_IP_AND_START_FILE_NAME}"]
"""
