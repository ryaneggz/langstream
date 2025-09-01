from nanoid import generate
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

from langgraph.types import StreamMode
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)


class LLMRequest(BaseModel):
    model: str = "openai:gpt-5-nano"
    system: str = "You are an elite AI assistant. You are helpful and friendly."
    thread_id: Optional[str] = Field(default_factory=lambda: f"thread_{generate()}")
    checkpoint_id: Optional[str] = Field(default=None)

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
    stream_mode: StreamMode | list[StreamMode] = "values"
