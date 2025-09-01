from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.config import RunnableConfig
from langgraph.prebuilt import create_react_agent

in_memory_checkpointer = InMemorySaver()


async def list_checkpoints(
    thread_id: str, checkpointer: BaseCheckpointSaver = in_memory_checkpointer
):
    config = RunnableConfig(configurable={"thread_id": thread_id})
    graph = create_react_agent("", [], checkpointer=checkpointer)
    checkpoints = []
    async for checkpoint in graph.aget_state_history(config):
        checkpoints.append(
            {
                **checkpoint.config,
                "values": checkpoint.values,
                "metadata": checkpoint.metadata,
                "parent_config": checkpoint.parent_config,
                "created_at": checkpoint.created_at,
            }
        )
    return checkpoints


async def fetch_checkpoint(
    thread_id: str,
    checkpoint_id: str | None = None,
    checkpointer: BaseCheckpointSaver = in_memory_checkpointer,
):
    config = RunnableConfig(
        configurable={"thread_id": thread_id, "checkpoint_id": checkpoint_id}
    )
    checkpoint = await checkpointer.aget(config)
    return checkpoint
