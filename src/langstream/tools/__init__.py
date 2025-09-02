import json
from langgraph.config import get_stream_writer
from langchain_core.runnables.config import RunnableConfig
from langgraph.config import get_store
from .code import python_code_interpreter
from ..services.memory import memory_service

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

async def get_user_info(config: RunnableConfig) -> str:
    """Look up user info."""
    user_info = await memory_service.get("user_1234")
    return json.dumps(user_info.dict())

TOOLS = [get_weather, get_user_info] + python_code_interpreter

