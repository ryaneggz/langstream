import json
from typing import List, Literal
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langgraph.types import StreamMode
from langgraph.config import get_stream_writer
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


##########################################################
## Utils
##########################################################
def convert_messages(payload: dict):
    # stream_mode: messages
    if isinstance(payload, tuple):
        return [payload[0], [payload[1][0].model_dump(), payload[1][1]]]

    converted: List[dict] = []

    if payload.get("payload"):
        if payload.get("payload", {}).get("input"):
            messages = payload.get("payload", {}).get("input").get("messages")
            for message in messages:
                converted.append(message.model_dump())
            payload["payload"]["input"]["messages"] = converted
            return payload
        if payload.get("payload", {}).get("result"):
            messages = payload.get("payload", {}).get("result")[0][1]
            for message in messages:
                converted.append(message.model_dump())
            payload["payload"]["result"][0] = [
                payload["payload"]["result"][0][0],
                converted,
            ]
            return payload

    if payload.get("messages"):
        messages = payload.get("messages")

    if payload.get("tools"):
        messages = payload.get("tools", {}).get("messages", [])

    if payload.get("agent"):
        messages = payload.get("agent", {}).get("messages", [])

    if not messages:
        raise ValueError("No messages found in payload")

    for message in messages:
        converted.append(message.model_dump())
    return converted


##########################################################
## Models
##########################################################
class LLMRequest(BaseModel):
    model: str = "openai:gpt-5-nano"
    system: str = "You are a helpful assistant"
    # stream_mode: StreamMode | list[StreamMode] = ["messages", "values"]
    stream_mode: Literal["values", "messages", "updates", "debug"] = "messages"

    class ChatMessage(BaseModel):
        role: Literal["user", "assistant", "system"]
        content: str

    messages: List[ChatMessage]

    def to_langchain_messages(self) -> List[BaseMessage]:
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
            else:
                raise ValueError(f"Unsupported role: {role}")
        return converted


##########################################################
## Tools
##########################################################
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


##########################################################
## FastAPI
##########################################################
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from fastapi-langgraph!"}


@app.get("/ping")
def health_check():
    return "pong"


@app.post("/llm/invoke")
async def llm_invoke(params: LLMRequest):
    agent = create_react_agent(
        model=params.model, tools=[get_weather], prompt=params.system
    )
    response = agent.invoke({"messages": params.to_langchain_messages()})
    return {"message": response}


@app.post("/llm/stream")
async def llm_stream(params: LLMRequest):
    agent = create_react_agent(
        model=params.model, tools=[get_weather], prompt=params.system
    )

    async def event_generator():
        try:
            async for chunk in agent.astream(
                {"messages": params.to_langchain_messages()},
                stream_mode=params.stream_mode,
            ):
                data = json.dumps(convert_messages(chunk))
                yield f"data: {data}\n\n"
        except Exception as e:
            error_msg = json.dumps({"error": str(e)})
            yield f"data: {error_msg}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
