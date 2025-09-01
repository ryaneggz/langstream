from fastapi import APIRouter, HTTPException

from ..models import ThreadSearch
from ..services.checkpoint import checkpoint_service

thread_router = APIRouter(prefix="/threads", tags=["Thread"])


@thread_router.post("/search", name="List Threads in Checkpointer")
async def search_threads(thread_search: ThreadSearch):
    return {
        "threads": await checkpoint_service.search_threads(thread_search=thread_search)
    }


@thread_router.get("/{thread_id}/checkpoints", name="List Checkpoints for Thread")
async def list_checkpoints(thread_id: str):
    checkpoints = await checkpoint_service.list_checkpoints(thread_id)
    if checkpoints is None:
        raise HTTPException(status_code=404, detail="Checkpoints not found")
    return {"checkpoints": checkpoints}


@thread_router.get(
    "/{thread_id}/checkpoint/{checkpoint_id}", name="Get Checkpoint for Thread"
)
async def get_checkpoint(thread_id: str, checkpoint_id: str):
    checkpoint = await checkpoint_service.get_checkpoint(thread_id, checkpoint_id)
    if checkpoint is None:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    return {"checkpoint": checkpoint}
