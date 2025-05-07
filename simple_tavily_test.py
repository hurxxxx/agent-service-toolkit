"""
Simple test script for the Tavily search functionality.

This script demonstrates how to use the Tavily search API directly.
"""

import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langchain.chat_models import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Check if Tavily API key is set
if not os.environ.get("TAVILY_API_KEY"):
    print("TAVILY_API_KEY environment variable is not set.")
    print("Please set it in your .env file or export it in your shell.")
    exit(1)

# Check if OpenAI API key is set
if not os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY environment variable is not set.")
    print("Please set it in your .env file or export it in your shell.")
    exit(1)

# Initialize the Tavily search tool
tavily_search = TavilySearch(
    max_results=3,
    topic="general",
    include_answer=True,
    include_raw_content=False,
    include_images=False,
    search_depth="basic",
)

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define a query
query = "What are the latest developments in AI in 2024?"
print(f"Searching for: {query}")
print("-" * 50)

# Perform the search
search_results = tavily_search.invoke({"query": query})
print("Search Results:")
print("-" * 50)
print(search_results)
print("-" * 50)

# Use the LLM to summarize the search results
system_message = """You are a helpful assistant that summarizes search results.
Please provide a concise summary of the search results provided."""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": f"Here are the search results for the query '{query}':\n\n{search_results}\n\nPlease summarize these results."}
]

print("Generating summary...")
print("-" * 50)
response = llm.invoke(messages)
print("Summary:")
print("-" * 50)
print(response.content)
