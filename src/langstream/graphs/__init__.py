from typing import Sequence, Union, Callable
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.store.base import BaseStore
from langgraph.graph.state import CompiledStateGraph

def graph_builder(
    graph_name: str = "react", 
    tools: Union[Sequence[Union[BaseTool, Callable]], ToolNode] = [], 
    prompt: str = "You are a helpful assistant.",
    model: str = "openai:gpt-5-nano",
    checkpointer: InMemorySaver | None = None,
    store: BaseStore | None = None,
) -> CompiledStateGraph:
    if graph_name == "react":
        return create_react_agent(
            model=model,
            tools=tools,
            prompt=prompt,
            checkpointer=checkpointer,
            store=store,
        )
        
    raise ValueError(f"Invalid graph name: {graph_name}")