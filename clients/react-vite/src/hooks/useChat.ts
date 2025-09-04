import { useRef, useState } from "react";

type StreamMode = "messages" | "values" | "updates" | "debug" | "tasks";

export default function useChat() {
	const responseRef = useRef("");
	const toolCallChunkRef = useRef("");
	const [messages, setMessages] = useState<any[]>([]);
	const [toolCall, setToolCall] = useState<any>({});
	// const [toolInput, setToolInput] = useState<any>('');
	// const [toolOutput, setToolOutput] = useState<any>('');
	// const [lastMessage, setLastMessage] = useState<any>('');

	const clearContent = () => {
		if (responseRef.current) {
			responseRef.current = "";
		}
		if (toolCallChunkRef.current) {
			toolCallChunkRef.current = "";
		}
	};

	const handleMessages = (payload: any, history: any[]) => {
		const response = payload[0];
		// Handle Tool Input
		if (response.tool_call_chunks && response.tool_call_chunks.length > 0) {
			toolCallChunkRef.current += response.tool_call_chunks[0].args;
			const existingIndex = history.findIndex((msg: any) => msg.id === response.id);

			// If the message already exists, update it
			if (existingIndex !== -1) {
			// Consolidate tool_call_chunks for the message with matching id
				const existingMsg = history[existingIndex];
				if (toolCallChunkRef.current) {
					try {
						existingMsg.input = JSON.parse(
							toolCallChunkRef.current
						);
					} catch {
						existingMsg.input = toolCallChunkRef.current;
					}
				}
				history[existingIndex] = {
					...existingMsg,
					...response,
				};
			} else {
					history.push({
						...response,
						input: toolCallChunkRef.current,
					});
			}
			setMessages((prev: any) => [...history]);
			return;
		}

		// Handle Final Response & Tool Response
		if (response.content && (!response.tool_call_chunks || response.tool_call_chunks.length === 0)) {
			const existingIndex = history.findIndex((msg: any) => msg.id === response.id);
			if (existingIndex !== -1) {
				// Always append to the related message content
				const existingMsg = history[existingIndex];
				const updatedContent = (existingMsg.content || "") + response.content;
				history[existingIndex] = {
					...existingMsg,
					...response,
					content: updatedContent,
				};
				setMessages((prev: any) => [...history]);
				return;
			} else {
				history.push({
					...response,
					content: response.content,
					role: response.type === "tool" ? "tool" : "assistant",
				});
				setMessages((prev: any) => [...history]);
				return;
			}
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
				setMessages
    };
}