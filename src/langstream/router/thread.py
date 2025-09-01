from fastapi import APIRouter

from ..services.checkpoint import fetch_checkpoint, list_checkpoints

thread_router = APIRouter(prefix="/thread", tags=["Thread"])


@thread_router.get("/{thread_id}/checkpoints", name="List Checkpoints for Thread")
async def get_thread(thread_id: str):
    return await list_checkpoints(thread_id)


@thread_router.get(
    "/{thread_id}/checkpoint/{checkpoint_id}", name="Get Checkpoint for Thread"
)
async def get_checkpoint(thread_id: str, checkpoint_id: str):
    return await fetch_checkpoint(thread_id, checkpoint_id)
