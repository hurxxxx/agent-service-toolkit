# Current Configuration Guide

This document provides an overview of the current successful configuration for the agent-service-toolkit project.

## Python Environment

The project now supports Python 3.11, 3.12, and 3.13. For the best experience, we recommend using Python 3.13 with conda for environment management.

## Package Management

We use `uv` for package management, which provides faster and more reliable dependency resolution than pip. The recommended approach is to use `uv sync` without the `--frozen` flag to ensure you get the latest compatible versions of all dependencies.

```bash
pip install uv
uv sync
source .venv/bin/activate
```

### Why avoid `--frozen`?

The `--frozen` flag forces `uv` to use the exact versions specified in the lock file (`uv.lock`). This can lead to downgrading packages if your lock file contains older versions than what you might have installed manually. By omitting the `--frozen` flag, `uv` will install the latest compatible versions within the constraints specified in `pyproject.toml`.

## Key Dependencies

The project relies on several key dependencies:

- **LangGraph**: Version 0.4.2 or later for the agent framework
- **LangChain**: Various components including langchain-core, langchain-community, etc.
- **Tavily Search**: The `langchain-tavily` package for web search functionality
- **FastAPI**: For the API service
- **Streamlit**: For the web interface

## OpenAI Models

The project now supports the latest OpenAI models, including:

- **gpt-4.1-mini**: Recommended as the default model for a good balance of performance and cost
- **gpt-4o**: For higher quality responses when needed
- Other models as specified in the `pyproject.toml` file

## Tavily Search Integration

The Tavily search agent provides more accurate and up-to-date search results compared to the default DuckDuckGo search. To use it:

1. Ensure you have a Tavily API key (sign up at https://app.tavily.com/sign-in)
2. Add your API key to your `.env` file:
   ```
   TAVILY_API_KEY=your_api_key_here
   ```
3. Use the agent by specifying `tavily-search-agent` in your requests

## Running the Service

The recommended way to start the service is:

```bash
python src/run_service.py
```

This will start the FastAPI service on the port specified in your `.env` file (default: 8080).

For the Streamlit interface, run in a separate terminal:

```bash
streamlit run src/streamlit_app.py
```

## WSL Networking

When running in a WSL environment, services bound to 0.0.0.0 might not be directly accessible using that address. You may need to:

1. Use the specific IP address of your WSL instance
2. Configure port forwarding if needed
3. Update the `HOST` and `PORT` settings in your `.env` file accordingly

## Testing

To run tests:

```bash
pytest
```

## Troubleshooting

If you encounter issues:

1. Check that your `.env` file contains the necessary API keys
2. Ensure you're using the recommended Python version
3. Try reinstalling dependencies with `uv sync` (without `--frozen`)
4. Check the logs for specific error messages

## Next Steps

Consider exploring:

1. Creating custom agents based on the existing templates
2. Integrating additional search or tool providers
3. Customizing the Streamlit interface for your specific use case
