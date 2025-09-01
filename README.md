# FastAPI LangGraph

A FastAPI web service for AI-powered conversations using LangGraph agents with multiple LLM providers.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- API keys for your chosen LLM providers (OpenAI, Anthropic, or Google)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd fastapi-langgraph
```

2. Install dependencies with uv:

```bash
uv sync
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
# Using the Makefile
make start

# Or with uv
uv run python -m src.langstream

# Or directly with Python (after uv sync)
python -m src.langstream

# Or with Uvicorn
uvicorn src.langstream.__main__:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/`.

## API Endpoints

### Health Check

```http
GET /ping
```

Returns `pong` for health monitoring.

### Synchronous Chat

```http
POST /llm/invoke
```

Send a message and receive a complete response:

```json
{
    "model": "openai:gpt-4",
    "system": "You are a helpful assistant.",
    "messages": [
        {
            "role": "user",
            "content": "What's the weather like in Dallas?"
        }
    ]
}
```

### Streaming Chat

```http
POST /llm/stream
```

Get real-time streaming responses with Server-Sent Events:

```json
{
    "model": "openai:gpt-4",
    "system": "You are a helpful assistant.",
    "stream_mode": "messages",
    "messages": [
        {
            "role": "user",
            "content": "What's the weather like in Dallas?"
        }
    ]
}
```

## Features

- **Multiple LLM Support**: Compatible with OpenAI, Anthropic, and Google Gemini models
- **Streaming & Sync APIs**: Choose between real-time streaming or traditional request-response patterns
- **LangGraph Integration**: Built-in tool calling capabilities with React agents
- **Multiple Stream Modes**: Support for tasks, debug, messages, and updates streaming modes
- **Health Check**: Built-in endpoint monitoring
- **Structured Logging**: Comprehensive logging with Loguru

## Stream Modes

- **`messages`** - Stream individual message updates
- **`tasks`** - Stream task execution progress
- **`debug`** - Stream detailed debugging information
- **`updates`** - Stream state updates from the agent

## Supported Models

Configure models using the format `provider:model-name`:

- **OpenAI**: `openai:gpt-4`, `openai:gpt-3.5-turbo`
- **Anthropic**: `anthropic:claude-3-sonnet`, `anthropic:claude-3-haiku`
- **Google**: `google:gemini-pro`, `google:gemini-pro-vision`

## Tools

The application includes sample tools:

- **Weather Tool**: Get weather information for cities (demo implementation)

Add custom tools in `src/langstream/tools/__init__.py`.

## Environment Variables

Required environment variables:

```bash
# At least one API key is required
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Development Roadmap

### Core Features
- [x] FastAPI application with sync and streaming endpoints
- [x] LangGraph agent integration with tool calling
- [x] Multi-provider LLM support (OpenAI, Anthropic, Google)
- [x] Multiple streaming modes (messages, tasks, debug, updates)
- [x] Structured logging with Loguru
- [x] Health check endpoint

### Planned Enhancements
- [ ] Authentication and authorization
- [ ] Request/response caching
- [ ] Persistent conversation history
- [ ] Docker containerization
- [ ] Integration tests and CI/CD pipeline

## Tech Stack

- **FastAPI** - Modern, fast web framework for Python APIs
- **LangGraph** - Advanced orchestration for multi-agent workflows
- **LangChain** - LLM integration and tool calling
- **Loguru** - Structured logging
- **Uvicorn** - ASGI server for production deployment

## Development

### Code Quality

```bash
# Format code
make format

# The project uses Ruff for linting and formatting
uvx ruff check
uvx ruff format
```

### Project Structure

```
src/
└── langstream/
    ├── __main__.py          # FastAPI application entry point
    ├── config/
    │   └── mocks/           # Mock data and responses
    ├── models/              # Data models and schemas
    ├── router/
    │   └── llm.py          # LLM endpoints and routing
    ├── tools/              # LangGraph tools and utilities
    │   └── __init__.py     # Tool definitions
    └── utils/              # Utility modules
        ├── logger.py       # Logging configuration
        └── stream.py       # Stream processing handlers
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make format` to format code
5. Submit a pull request

## License

This project is licensed under the MIT License.