from fastapi.openapi.models import Example


class Examples:
    THREAD_SEARCH_EXAMPLES = {
        "list_threads": Example(
            summary="list_threads",
            description="List Threads in Checkpointer",
            value={"limit": 10, "offset": 0, "metadata": {}},
        ),
        "list_checkpoints": Example(
            summary="list_checkpoints",
            description="List Checkpoints for Thread",
            value={"limit": 10, "offset": 0, "metadata": {"thread_id": "thread_123"}},
        ),
        "get_checkpoint": Example(
            summary="get_checkpoint",
            description="Get Checkpoint for Thread",
            value={
                "limit": 10,
                "offset": 0,
                "metadata": {
                    "thread_id": "thread_123",
                    "checkpoint_id": "checkpoint_123",
                },
            },
        ),
    }
    
    LLM_INVOKE_EXAMPLES = {
        "stateless_invoke": Example(
            summary="stateless_invoke",
            description="LLM Stateless",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "messages": [
                    {
                        "role": "user",
                        "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
        "persistant_thread": Example(
            summary="persistent_thread",
            description="LLM with Persistant Thread",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "metadata": {
                    "thread_id": "thread_CkzLFPHdZX8ID6iZSP9pj"
                },
                "messages": [
                    {
                        "role": "user",
                        "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
        "branch_from_checkpoint": Example(
            summary="branch_from_checkpoint",
            description="Invoke LLM",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "metadata": {
                    "thread_id": "thread_CkzLFPHdZX8ID6iZSP9pj",
                    "checkpoint_id": "6fb4c17e-ff1d-46ca-af6d-ff289a019423"
                },
                "messages": [
                    {
                    "role": "user",
                    "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
    }
    
    LLM_STREAM_EXAMPLES = {
        "stateless_stream": Example(
            summary="stateless_stream",
            description="LLM Stateless",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "stream_mode": "messages",
                "messages": [
                    {
                        "role": "user",
                        "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
        "persistant_thread": Example(
            summary="persistant_thread",
            description="LLM with Persistant Thread",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "stream_mode": "messages",
                "metadata": {
                    "thread_id": "thread_CkzLFPHdZX8ID6iZSP9pj"
                },
                "messages": [
                    {
                        "role": "user",
                        "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
        "branch_from_checkpoint": Example(
            summary="branch_from_checkpoint",
            description="LLM with Branch from Checkpoint",
            value={
                "model": "openai:gpt-5-nano",
                "system": "You are a helpful assistant.",
                "stream_mode": "messages",
                "metadata": {
                    "thread_id": "thread_CkzLFPHdZX8ID6iZSP9pj",
                    "checkpoint_id": "6fb4c17e-ff1d-46ca-af6d-ff289a019423"
                },
                "messages": [
                    {
                        "role": "user",
                        "content": "Weather in Dallas?"
                    }
                ]
            }
        ),
    }
