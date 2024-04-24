import json
import os

from data_compressor.config import Config
from data_compressor.context.compression import ContextCompressor
import asyncio
from data_compressor.memory import Memory

async def _get_similar_content_by_query(query, pages, azure_endpoint):

    # Summarize Raw Data
    memory = Memory(Config().embedding_provider, azure_endpoint)
    context_compressor = ContextCompressor(documents=pages, embeddings=memory.get_embeddings())
    # Run Tasks
    return await context_compressor.aget_context(query, max_results=8)

async def compress_data_by_query(query,page,azure_open_api_key, azure_endpoint):
    os.environ["AZURE_OPENAI_API_KEY"] = azure_open_api_key
    return await _get_similar_content_by_query(query, page, azure_endpoint)

async def _main():
    azure_open_api_key = "a958115c7d544521bd8ac3176d5475ad"
    azure_endpoint = "https://zunoassistnew.openai.azure.com/"

    # Call the coroutine function using await

    with open("C:/Users/NimishaBansal/Downloads/compression_sample.json", "r",
              encoding="utf-8") as file:
        # Read the entire contents of the file
        file_contents = json.load(file)

    # print(type(file_contents))
    result = await compress_data_by_query("Chatbot document integration design", file_contents,
                                                          azure_open_api_key, azure_endpoint)
    print(result)
    # Use the result here


# Run the main coroutine function
if __name__ == "__main__":
    asyncio.run(_main())