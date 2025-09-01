from fastapi import APIRouter

from ..services.checkpoint import checkpoint_service

thread_router = APIRouter(prefix="/threads", tags=["Thread"])


@thread_router.get("", name="List Threads in Checkpointer")
async def list_threads(limit: int = 1000):
    return await checkpoint_service.list_threads(limit=limit)


@thread_router.get("/{thread_id}/checkpoints", name="List Checkpoints for Thread")
async def list_checkpoints(thread_id: str):
    return await checkpoint_service.list_checkpoints(thread_id)


@thread_router.get(
    "/{thread_id}/checkpoint/{checkpoint_id}", name="Get Checkpoint for Thread"
)
async def get_checkpoint(thread_id: str, checkpoint_id: str):
    return await checkpoint_service.get_checkpoint(thread_id, checkpoint_id)
