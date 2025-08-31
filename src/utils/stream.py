from langgraph.types import StreamMode
from typing import List

def handle_tasks_mode(payload: dict):
    converted: List[dict] = []
    
    if 'input' in payload:
        input = payload['input']
        if 'messages' in payload['input']:
            for message in input['messages']:
                converted.append(message.model_dump())
            input['messages'] = converted
        return payload
    
    if 'result' in payload:
        messages = payload['result'][0][1]
        for message in messages:
            converted.append(message.model_dump())
        payload['result'][0] = [payload['result'][0][0], converted]
    
    return payload

def convert_messages(
    payload: dict, stream_mode: StreamMode | list[StreamMode] | None = None
):
    if stream_mode == "tasks":
        return handle_tasks_mode(payload)
    
    # stream_mode: messages
    if isinstance(payload, tuple):
        return [payload[0].model_dump(), payload[1]]

    converted: List[dict] = []

    # stream_mode: debug
    if payload.get("payload"):
        if payload.get("payload", {}).get("input"):
            input = payload.get("payload", {}).get("input")

            if "messages" in input:
                for message in input.get("messages"):
                    converted.append(message.model_dump())
                payload["payload"]["input"]["messages"] = converted
                return payload

            if "args" in input[0]:
                return payload

        if payload.get("payload", {}).get("result"):
            messages = payload.get("payload", {}).get("result")[0][1]
            for message in messages:
                converted.append(message.model_dump())
            payload["payload"]["result"][0] = [
                payload["payload"]["result"][0][0],
                converted,
            ]
            return payload

    if payload.get("messages"):
        messages = payload.get("messages")

    # stream_mode: updates
    if payload.get("agent"):
        messages = payload.get("agent", {}).get("messages", [])

    # stream_mode: updates
    if payload.get("tools"):
        messages = payload.get("tools", {}).get("messages", [])

    if not messages:
        raise ValueError("No messages found in payload")

    for message in messages:
        converted.append(message.model_dump())
    return converted
