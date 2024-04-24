import json
import os

from config import Config
from context.compression import ContextCompressor
import asyncio
from memory import Memory

async def _get_similar_content_by_query(query, pages, azure_endpoint):

    # Summarize Raw Data
    memory = Memory(Config().embedding_provider, azure_endpoint)
    context_compressor = ContextCompressor(documents=pages, embeddings=memory.get_embeddings())
    # Run Tasks
    return await context_compressor.aget_context(query, max_results=8)

async def compress_data_by_query(query,page,azure_open_api_key, azure_endpoint):
    os.environ["AZURE_OPENAI_API_KEY"] = azure_open_api_key
    return await _get_similar_content_by_query(query, page, azure_endpoint)

