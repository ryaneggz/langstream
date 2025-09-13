from fastapi import APIRouter, HTTPException, Body

from ..models import ThreadSearch
from ..services.checkpoint import checkpoint_service
from ..config.examples import Examples

thread_router = APIRouter(prefix="/threads", tags=["Thread"])


@thread_router.post("/search", name="Query Threads in Checkpointer")
async def search_threads(
    thread_search: ThreadSearch = Body(
        openapi_examples=Examples.THREAD_SEARCH_EXAMPLES
    ),
):
    metadata = thread_search.model_dump().get("metadata", {})

    if "thread_id" in metadata and not "checkpoint_id" in metadata:
        thread_id = metadata["thread_id"]
        checkpoints = await checkpoint_service.list_checkpoints(thread_id)
        if checkpoints is None:
            raise HTTPException(status_code=404, detail="Checkpoints not found")
        return {"checkpoints": checkpoints}
    if "thread_id" in metadata and "checkpoint_id" in metadata:
        thread_id = metadata["thread_id"]
        checkpoint_id = metadata["checkpoint_id"]
        checkpoint = await checkpoint_service.get_checkpoint(thread_id, checkpoint_id)
        if checkpoint is None:
            raise HTTPException(status_code=404, detail="Checkpoint not found")
        return {"checkpoint": checkpoint}
    return {
        "threads": await checkpoint_service.search_threads(thread_search=thread_search)
    }


@thread_router.delete("/{thread_id}", name="Delete Thread")
async def delete_thread(thread_id: str):
    success = await checkpoint_service.delete_thread(thread_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"message": f"Thread {thread_id} deleted successfully"}
