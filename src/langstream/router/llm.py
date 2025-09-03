import json
from typing import Any

from fastapi import status, APIRouter, Body
from fastapi.responses import StreamingResponse, Response

from langchain_core.runnables.config import RunnableConfig

from ..graphs import graph_builder
from ..config.examples import Examples
from ..tools import TOOLS
from ..config.mocks.response import MockResponse
from ..utils.stream import convert_messages
from ..utils.logger import logger
from ..models import LLMRequest, LLMStreamRequest
from ..services.checkpoint import in_memory_checkpointer
from ..services.memory import in_memory_store, memory_service
from ..graphs import add_memories_to_system
from ..tools.memory import save_memory, search_memory

llm_router = APIRouter(prefix="/llm", tags=["LLM"])

async def construct_agent(params: LLMRequest|LLMStreamRequest):
    # Add config if it exists
    config = (
        RunnableConfig(configurable=params.metadata.model_dump())
        if params.metadata
        else None
    )
    
    if config:
        ## Construct the prompt
        memory_prompt = await add_memories_to_system()
        prompt = params.system + "\n" + memory_prompt if memory_prompt else params.system
        tools = TOOLS + [save_memory]

    # Asynchronous LLM call
    agent = graph_builder(
        graph_name="react",
        model=params.model,
        tools=tools,
        prompt=prompt,
        checkpointer=in_memory_checkpointer if config else None,
        store=in_memory_store if config else None,
    )
    return agent, config


@llm_router.post(
    "/invoke",
    responses={status.HTTP_200_OK: MockResponse.INVOKE_RESPONSE},
    name="Invoke Graph",
)
async def llm_invoke(
    params: LLMRequest = Body(openapi_examples=Examples.LLM_INVOKE_EXAMPLES)
) -> dict[str, Any] | Any:
    agent, config = await construct_agent(params)

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
async def llm_stream(
    params: LLMStreamRequest = Body(openapi_examples=Examples.LLM_STREAM_EXAMPLES)
) -> StreamingResponse:
    agent, config = await construct_agent(params)

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
