from langgraph.config import get_stream_writer
from langchain_sandbox import PyodideSandboxTool


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    import random

    templates = [
        f"It's always sunny in {city}!",
        f"The weather in {city} is perfect for a walk.",
        f"{city} is experiencing clear skies today.",
        f"Expect sunshine and smiles in {city}.",
        f"{city} has beautiful weather right now.",
    ]
    return random.choice(templates)


python_code_sandbox = PyodideSandboxTool(
    # Allow Pyodide to install python packages that
    # might be required.
    allow_net=True
)

TOOLS = [get_weather, python_code_sandbox]
