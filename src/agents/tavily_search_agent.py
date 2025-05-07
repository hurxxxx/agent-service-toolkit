"""
Tavily Search Agent using LangGraph.

This module implements a search agent that uses Tavily for web search functionality.
The agent is built using LangGraph and follows a simple workflow:
1. Receive a user query
2. Process the query using an LLM
3. Use Tavily search when needed
4. Return a response to the user
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from core import get_model, settings


class AgentState(MessagesState, total=False):
    """State for the Tavily search agent.

    Extends MessagesState to store conversation history.
    Uses `total=False` to make all fields optional.
    """
    remaining_steps: int


# Initialize Tavily search tool
tavily_search = TavilySearch(
    max_results=3,
    topic="general",
    include_answer=True,
    include_raw_content=False,
    include_images=False,
    search_depth="basic",
)

# List of tools available to the agent
tools = [tavily_search]


def get_system_message() -> str:
    """Return the system message for the agent."""
    return """You are a helpful search assistant with access to the Tavily search engine.

When a user asks a question that requires up-to-date information or facts that you're unsure about,
use the Tavily search tool to find relevant information.

Follow these guidelines:
1. For factual questions, use the search tool to find accurate information
2. Cite your sources by including links from the search results
3. If search results don't provide relevant information, acknowledge the limitations
4. Synthesize information from multiple sources when appropriate
5. Be concise and direct in your responses
6. For questions that don't require search (like simple greetings or opinions), respond directly

Always be helpful, accurate, and respectful of the user's time.
"""


async def acall_model(state: AgentState, config: RunnableConfig) -> AgentState:
    """Call the language model with the current state.

    Args:
        state: The current state of the agent
        config: Configuration for the runnable

    Returns:
        Updated state with the model's response
    """
    # Get the model from settings or config
    model_name = config["configurable"].get("model", settings.DEFAULT_MODEL)
    model = get_model(model_name)

    # Add system message if it's not already in the messages
    messages = state["messages"]
    if not messages or not any(m.type == "system" for m in messages):
        system_message = get_system_message()
        messages = [{"type": "system", "content": system_message}] + messages

    # Bind tools to the model
    model_with_tools = model.bind_tools(tools)

    # Generate a response
    response = await model_with_tools.ainvoke(messages, config)

    # Check if we have enough steps remaining
    remaining = state.get("remaining_steps", 10)
    if remaining < 2 and response.tool_calls:
        return {
            "messages": [
                AIMessage(content="I need more steps to process this request properly.")
            ]
        }

    # Return the response
    return {"messages": [response], "remaining_steps": remaining - 1}


# Define the graph
def build_tavily_search_agent() -> StateGraph:
    """Build and return the Tavily search agent graph."""
    # Create the graph
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node("model", acall_model)
    graph_builder.add_node("tools", ToolNode(tools))

    # Set entry point
    graph_builder.set_entry_point("model")

    # Add edges
    graph_builder.add_conditional_edges(
        "model",
        tools_condition,
        {
            "tools": "tools",
            "end": END,
        },
    )
    graph_builder.add_edge("tools", "model")

    # Compile the graph
    return graph_builder.compile(checkpointer=MemorySaver())


# Create the agent
tavily_search_agent = build_tavily_search_agent()
