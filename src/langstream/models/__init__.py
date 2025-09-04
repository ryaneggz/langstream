from nanoid import generate
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Any, Callable
from langchain_core.tools import BaseTool
from uuid import uuid4
from nanoid import generate

from langgraph.types import StreamMode
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)


class Config(BaseModel):
    thread_id: Optional[str] = Field(
        ..., description="The thread id", examples=[f"thread_{generate()}"]
    )
    checkpoint_id: Optional[str] = Field(
        default=None, description="The checkpoint id", examples=[str(uuid4())]
    )
    graph_id: Optional[Literal["react","deepagent"]] = Field(
        default=None, description="The graph id", examples=["react", "deepagent"]
    )


class ThreadSearch(BaseModel):
    limit: int = Field(default=100, description="The limit of threads to search")
    offset: int = Field(default=0, description="The offset of threads to search")
    metadata: Optional[dict] = Field(
        default=None, description="The metadata of threads to search"
    )


class LLMRequest(BaseModel):
    model: str = "openai:gpt-5-nano"
    system: str = "You are a helpful assistant."
    tools: list[BaseTool | Callable | dict[str, Any]] = []
    metadata: Optional[Config] = Field(
        default=None, description="LangGraph configuration"
    )

    class ChatMessage(BaseModel):
        role: Literal["user", "assistant", "system", "tool"] = Field(examples=["user"])
        content: str = Field(examples=["Weather in Dallas?"])

    messages: List[ChatMessage]

    def to_langchain_messages(self) -> List[BaseMessage]:
        # Convert API messages to LangChain message objects
        converted: List[BaseMessage] = []
        for message in self.messages:
            role = message.role
            content = message.content
            if role == "user":
                converted.append(HumanMessage(content=content))
            elif role == "assistant":
                converted.append(AIMessage(content=content))
            elif role == "system":
                converted.append(SystemMessage(content=content))
            elif role == "tool":
                converted.append(ToolMessage(content=content))
            else:
                raise ValueError(f"Unsupported role: {role}")
        return converted


class LLMStreamRequest(LLMRequest):
    stream_mode: StreamMode | list[StreamMode] = "messages"
