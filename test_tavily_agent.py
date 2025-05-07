"""
Test script for the Tavily search agent.

This script demonstrates how to use the Tavily search agent to perform web searches.
"""

import asyncio
import os
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

# Load environment variables from .env file
load_dotenv()

# Import the agent
from agents.agents import get_agent

# Check if Tavily API key is set
if not os.environ.get("TAVILY_API_KEY"):
    print("TAVILY_API_KEY environment variable is not set.")
    print("Please set it in your .env file or export it in your shell.")
    exit(1)

# Get the Tavily search agent
agent = get_agent("tavily-search-agent")


async def main():
    """Run a test query with the Tavily search agent."""
    # Create a unique thread ID for this conversation
    thread_id = str(uuid4())

    # Define the query
    query = "What are the latest developments in AI in 2024?"

    # Create the input state with the query
    input_state = {
        "messages": [HumanMessage(content=query)]
    }

    # Create the configuration
    config = RunnableConfig(
        configurable={"thread_id": thread_id}
    )

    print(f"Sending query: {query}")
    print("-" * 50)

    # Invoke the agent
    result = await agent.ainvoke(input_state, config)

    # Print the result
    print("Agent response:")
    print("-" * 50)
    for message in result["messages"]:
        message.pretty_print()

    # Ask a follow-up question
    follow_up = "Can you tell me more about AI safety regulations?"

    print(f"\nSending follow-up query: {follow_up}")
    print("-" * 50)

    # Create the input state with the follow-up query
    follow_up_input = {
        "messages": [HumanMessage(content=follow_up)]
    }

    # Invoke the agent again with the same thread_id to maintain conversation context
    follow_up_result = await agent.ainvoke(follow_up_input, config)

    # Print the result
    print("Agent response to follow-up:")
    print("-" * 50)
    for message in follow_up_result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())
