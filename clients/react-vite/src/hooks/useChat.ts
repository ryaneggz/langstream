import { useRef, useState } from "react";
import { SSE } from "sse.js";

type StreamMode = "messages" | "values" | "updates" | "debug" | "tasks";

const in_mem_messages: any[] = [];

export type ChatContextType = {
	responseRef: React.RefObject<string>;
	toolCallChunkRef: React.RefObject<string>;
	query: string;
	setQuery: (query: string) => void;
	handleSubmit: () => void;
	sseHandler: (payload: any, messages: any[], stream_mode: StreamMode | Array<StreamMode>) => void;
	clearContent: () => void;
	messages: any[];
	setMessages: (messages: any[]) => void;
	metadata: string;
	setMetadata: (metadata: string) => void;
}

export default function useChat(): ChatContextType {
	const responseRef = useRef("");
	const toolCallChunkRef = useRef("");
	const [query, setQuery] = useState("");
	const [messages, setMessages] = useState<any[]>([]);
	const [metadata, setMetadata] = useState(() => {
		const threadId = `thread_${Math.random().toString(36).substring(2, 15)}`;
		return JSON.stringify({ thread_id: threadId }, null, 2);
	});

	const handleSSE = (query: string, model: string = "openai:gpt-5-nano") => {
		// Add user message to the existing messages state
		const userMessage = {
			id: `user-${Date.now()}`,
			model: model,
			content: query,
			role: "user",
			type: "user",
		};

		const updatedMessages = [...messages, userMessage];
		setMessages(updatedMessages);

		// Add user message to in-memory messages for SSE handling
		in_mem_messages.push(userMessage);

		clearContent();
		const options = {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Accept: "text/event-stream",
			},
			payload: JSON.stringify({
				model: model,
				stream_mode: "messages",
				system: "You are a helpful assistant.",
				metadata: JSON.parse(metadata),
				messages: updatedMessages
					.filter(
						(msg) => msg.role === "user" || msg.role === "assistant"
					)
					.map((msg) => ({
						role: msg.role,
						content: msg.content,
					})),
			}),
		};
		const source = new SSE("http://localhost:8000/llm/stream", options);
		source.addEventListener("message", function (e: any) {
			// Assuming we receive JSON-encoded data payloads:
			const payload = JSON.parse(e.data);
			sseHandler(payload, in_mem_messages, "messages");
		});

		source.addEventListener("error", (e: any) => {
			console.error("Error:", e);
		});
	};

	const handleSubmit = () => {
		console.log("Submitted:", query);
		handleSSE(query);
		setQuery("");
	};

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
						existingMsg.input = JSON.parse(toolCallChunkRef.current);
					} catch {
						try {
							const autoAddCommas = "[" + toolCallChunkRef.current.replace(/}\s*{/g, "},{") + "]";
							existingMsg.input = JSON.parse(autoAddCommas);
						} catch {
							existingMsg.input = toolCallChunkRef.current;
						}
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
		handleSubmit,
		sseHandler,
		clearContent,
		query,
		setQuery,
		messages,
		setMessages,
		metadata,
		setMetadata,
	};
}