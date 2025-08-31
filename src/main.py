import json
from loguru import logger
from typing import List, Literal
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from langgraph.types import StreamMode
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import (
	BaseMessage,
	HumanMessage,
	AIMessage,
	SystemMessage,
	ToolMessage,
)

from src.tools import TOOLS
from src.utils.stream import convert_messages
from src.utils.logger import logger

# Request/response models
class LLMRequest(BaseModel):
	model: str = "openai:gpt-5-nano"
	system: str = (
		"You are an elite AI assistant. "
		"You are helpful and friendly."
	)
	stream_mode: StreamMode | list[StreamMode] | None = None

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

# Initialize FastAPI app
app = FastAPI(docs_url="/")

@app.get("/ping")
def health_check():
	# Health check endpoint
	return "pong"

@app.post("/llm/invoke")
async def llm_invoke(params: LLMRequest):
	# Synchronous LLM call
	agent = create_react_agent(model=params.model, tools=TOOLS, prompt=params.system)
	response = agent.invoke({"messages": params.to_langchain_messages()})
	return {"message": response}

@app.post("/llm/stream")
async def llm_stream(params: LLMRequest):
	# Streaming LLM call
	agent = create_react_agent(model=params.model, tools=TOOLS, prompt=params.system)

	async def event_generator():
		try:
			# Stream LLM output chunks as server-sent events
			async for chunk in agent.astream(
				{"messages": params.to_langchain_messages()},
				stream_mode=params.stream_mode,
			):
				data = json.dumps(
					convert_messages(chunk, stream_mode=params.stream_mode)
				)
				yield f"data: {data}\n\n"
		except Exception as e:
			# Log and stream error if occurs
			logger.exception("Error in event_generator: %s", e)
			error_msg = json.dumps({"error": str(e)})
			yield f"data: {error_msg}\n\n"

	return StreamingResponse(
		event_generator(),
		media_type="text/event-stream",
		headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
	)

if __name__ == "__main__":
	import uvicorn
	# Run FastAPI app with Uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)
