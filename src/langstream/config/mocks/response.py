from . import *


class MockResponse:
    INVOKE_RESPONSE = {
        "description": "Chat completion response.",
        "content": {
            "application/json": {"example": INVOKE_MOCK},
        },
    }
    STREAM_RESPONSE = {
        "description": "Latest message from existing thread.",
        "content": {
            "text/event-stream": {
                "schema": {"type": "string", "format": "binary"},
                "examples": {
                    "values": {
                        "summary": "stream_mode: values",
                        "value": STREAM_VALUES_MOCK,
                    },
                    "messages": {
                        "summary": "stream_mode: messages",
                        "value": STREAM_MESSAGES_MOCK,
                    },
                    "updates": {
                        "summary": "stream_mode: updates",
                        "value": STREAM_UPDATES_MOCK,
                    },
                    "debug": {
                        "summary": "stream_mode: debug",
                        "value": STREAM_DEBUG_MOCK,
                    },
                    "tasks": {
                        "summary": "stream_mode: tasks",
                        "value": STREAM_TASKS_MOCK,
                    },
                    ## TODO: Did not see a response initially for this
                    # "checkpoints": {
                    #     "summary": "stream_mode: checkpoints",
                    #     "value": STREAM_CHECKPOINTS_MOCK
                    # },
                },
            }
        },
    }
