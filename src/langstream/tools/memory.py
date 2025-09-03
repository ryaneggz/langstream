
from nanoid import generate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from ..services.memory import memory_service
 
@tool
async def save_memory(
    memory: str, 
    ttl: int | None = None, 
    config: RunnableConfig | None = None
) -> str:
	"""
    Toolkit: Memory
    Description: Save memory to vectorstore for later semantic retrieval.
	Args:
		memory: The memory to save.
		ttl: The time to live for the memory.
		config: The config for the memory.
	Returns:
		The memory ID.
	"""
	memory_id = f"memory_{generate()}"
	await memory_service.set(memory_id, {"memory": memory}, ttl=ttl)
	return f"Memory ID {memory_id} saved."

@tool
async def search_memory(
    query: str,
    config: RunnableConfig | None = None
) -> str:
	"""
    Toolkit: Memory
    Description: Search for memories based on a query.
	Args:
		query: The query to search for.
		config: The config for the memory.
	Returns:
		The memories (documents).
	"""
	return await memory_service.search()