from fastapi import APIRouter
import uuid


thread_router = APIRouter(prefix="/thread", tags=["Thread"])


def gen_thread_id():
    return str(uuid.uuid4())


@thread_router.get("/{thread_id}")
async def list_threads():
    return {"message": "Thread"}
