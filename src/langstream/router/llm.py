import json
from typing import Any

from fastapi import status, APIRouter
from fastapi.responses import StreamingResponse, Response

from langgraph.prebuilt import create_react_agent
from langchain_core.runnables.config import RunnableConfig

from ..tools import TOOLS
from ..config.mocks.response import MockResponse
from ..utils.stream import convert_messages
from ..utils.logger import logger
from ..models import LLMRequest, LLMStreamRequest
from ..services.checkpoint import in_memory_checkpointer

llm_router = APIRouter(prefix="/llm", tags=["LLM"])


@llm_router.post(
    "/invoke",
    responses={status.HTTP_200_OK: MockResponse.INVOKE_RESPONSE},
    name="Invoke Graph",
)
async def llm_invoke(params: LLMRequest) -> dict[str, Any] | Any:
    # Add config if it exists
    config = (
        RunnableConfig(configurable=params.config.model_dump())
        if params.config
        else None
    )

    # Asynchronous LLM call
    agent = create_react_agent(
        model=params.model,
        tools=TOOLS,
        prompt=params.system,
        checkpointer=in_memory_checkpointer if config else None,
    )

    # Invoke the agent
    response = await agent.ainvoke(
        {"messages": params.to_langchain_messages()},
        config=config,
    )
    return response


@llm_router.post(
    "/stream",
    response_class=Response,
    responses={status.HTTP_200_OK: MockResponse.STREAM_RESPONSE},
    name="Stream Graph",
)
async def llm_stream(params: LLMStreamRequest) -> StreamingResponse:
    # Add config if it exists
    config = (
        RunnableConfig(configurable=params.config.model_dump())
        if params.config
        else None
    )
    # Streaming LLM call
    agent = create_react_agent(
        model=params.model,
        tools=TOOLS,
        prompt=params.system,
        checkpointer=in_memory_checkpointer if config else None,
    )

    # Event generator
    async def event_generator():
        try:
            # Stream LLM output chunks as server-sent events
            async for chunk in agent.astream(
                {"messages": params.to_langchain_messages()},
                config=config,
                stream_mode=params.stream_mode,
            ):
                # Convert the chunk to a JSON string
                data = json.dumps(
                    convert_messages(chunk, stream_mode=params.stream_mode)
                )
                yield f"data: {data}\n\n"
        except Exception as e:
            # Log and stream error if occurs
            logger.exception("Error in event_generator: %s", e)
            error_msg = json.dumps({"error": str(e)})
            yield f"data: {error_msg}\n\n"

    # Return the streaming response
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
