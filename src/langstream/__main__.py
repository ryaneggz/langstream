import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router.llm import llm_router
from .router.thread import thread_router

# Initialize FastAPI app
app = FastAPI(
    title="LangStream",
    description=(
        "LangStream is a fastAPI web service for AI-powered "
        "conversations using LangGraph agents with multiple LLM providers."
    ),
    version=os.getenv("APP_VERSION", "0.1.0"),
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router)
app.include_router(thread_router)

if __name__ == "__main__":
    import uvicorn

    # Run FastAPI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
