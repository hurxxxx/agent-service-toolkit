# Tavily Search Agent

This document provides an overview of the Tavily search agent implementation in the agent-service-toolkit.

## Overview

The Tavily search agent is a specialized agent that uses the Tavily search API to perform web searches and provide relevant information to users. It is built using LangGraph, a framework for creating complex, multi-step AI workflows.

## Implementation Details

The agent is implemented in `src/agents/tavily_search_agent.py` and follows a simple workflow:

1. Receive a user query
2. Process the query using an LLM
3. Use Tavily search when needed
4. Return a response to the user

### Key Components

- **State Management**: The agent uses a custom state class that extends `MessagesState` to store conversation history.
- **Tavily Search Tool**: The agent uses the `TavilySearch` tool from the `langchain-tavily` package to perform web searches.
- **LLM Integration**: The agent uses the language model specified in the settings or configuration to process user queries and generate responses.
- **Graph Structure**: The agent uses a simple graph structure with two main nodes: `model` and `tools`.

### Configuration

The Tavily search tool is configured with the following parameters:

```python
tavily_search = TavilySearch(
    max_results=3,
    topic="general",
    include_answer=True,
    include_raw_content=False,
    include_images=False,
    search_depth="basic",
)
```

These parameters can be adjusted based on your specific needs.

## Usage

To use the Tavily search agent, you need to:

1. Set the `TAVILY_API_KEY` environment variable in your `.env` file.
2. Select the agent when making requests to the service.

Example:

```python
from agents.agents import get_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from uuid import uuid4

# Get the Tavily search agent
agent = get_agent("tavily-search-agent")

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

# Invoke the agent
result = await agent.ainvoke(input_state, config)

# Print the result
for message in result["messages"]:
    message.pretty_print()
```

## Dependencies

The Tavily search agent requires the following dependencies:

- `langchain-tavily`: For the Tavily search functionality
- `langgraph`: For the graph-based agent architecture
- `langchain-core`: For the core LangChain functionality

## API Key

To use the Tavily search agent, you need to obtain an API key from Tavily. You can sign up for an API key at [https://app.tavily.com/sign-in](https://app.tavily.com/sign-in).

Once you have an API key, add it to your `.env` file:

```
TAVILY_API_KEY=your_api_key_here
```

## Customization

You can customize the Tavily search agent by modifying the following:

- **System Message**: Change the system message to adjust the agent's behavior and instructions.
- **Search Parameters**: Adjust the parameters of the Tavily search tool to change the search behavior.
- **Graph Structure**: Modify the graph structure to add additional nodes or edges for more complex workflows.

## Troubleshooting

If you encounter issues with the Tavily search agent, check the following:

1. Make sure the `TAVILY_API_KEY` environment variable is set correctly.
2. Ensure that the `langchain-tavily` package is installed and up-to-date.
3. Check the logs for any error messages related to the Tavily API or the agent.

## References

- [Tavily API Documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
