import { useRef, useState } from "react";

type StreamMode = "messages" | "values" | "updates" | "debug" | "tasks";

export default function useChat() {
	const responseRef = useRef("");
	const toolCallChunkRef = useRef("");
	const [messages, setMessages] = useState<any[]>([]);
	const [toolCall, setToolCall] = useState<any>({});
	const [toolInput, setToolInput] = useState<any>('');
	const [toolOutput, setToolOutput] = useState<any>('');
	const [lastMessage, setLastMessage] = useState<any>('');

	const clearContent = () => {
		if (responseRef.current) {
			responseRef.current = "";
		}
		if (toolCallChunkRef.current) {
			toolCallChunkRef.current = "";
		}
	};

	const handleMessages = (payload: any, messages: any[]) => {
		const response = payload[0];

		// Handle tool call
		if (response.tool_call_chunks && response.tool_call_chunks.length > 0) {
			toolCallChunkRef.current += response.tool_call_chunks[0].args;
			const existingIndex = messages.findIndex((msg: any) => msg.id === response.id);
			if (existingIndex !== -1) {
				// Consolidate tool_call_chunks for the message with matching id
				const existingMsg = messages[existingIndex];
				if (toolCallChunkRef.current) {
					try {
						setToolInput(toolCallChunkRef.current);
						existingMsg.input = JSON.parse(toolCallChunkRef.current);
					} catch {
						setToolInput(toolCallChunkRef.current);
						existingMsg.input = toolCallChunkRef.current;
					}
				}
				messages[existingIndex] = { ...existingMsg, ...response };
			} else {
				messages.push(response);
			}
			return messages;
		}
		
		// Handle AI response
		if (response.content) {
			responseRef.current += response.content;
			
			const existingIndex = messages.findIndex(
                (msg: any) => msg.id === response.id
            );
			if (existingIndex !== -1) {
				const existingMsg = messages[existingIndex];
				existingMsg.content = responseRef.current;
				messages[existingIndex] = { ...existingMsg };
			} else {
				messages.push(response);
			}
			if (response.type === "tool") {
				setToolOutput(responseRef.current);
				clearContent();
			} else {
				setLastMessage(responseRef.current);
			}
			return messages;
		}
	};

	function sseHandler(
			payload: any,
			messages: any[],
			stream_mode: StreamMode | Array<StreamMode> = "messages"
    ) {
			if (stream_mode === "messages" || stream_mode.includes("messages")) {
				console.log("messages: ", payload);
				handleMessages(payload, messages);
			}
    }

	return {
        responseRef,
        toolCallChunkRef,
        sseHandler,
        clearContent,
				setToolCall,
				toolCall,
        messages,
				setMessages,
				lastMessage,
				toolInput,
				toolOutput,
    };
}