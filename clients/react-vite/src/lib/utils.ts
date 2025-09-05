import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs))
}

export function formatMessages(messages: any[]) {
	return messages.map((message: any) => {
		if (["user", "human"].includes(message.type)) {
			return {
				...message,
				role: "user",
			};
		}
		if (["assistant", "ai"].includes(message.type) && !message.tool_calls?.length) {
			return {
				...message,
				role: "assistant",
			};
		}
		if (["assistant", "ai"].includes(message.type) && message.tool_calls?.length) {
			const input = message.tool_calls.map((tool_call: any) => {
				return {
					...tool_call.args,
				};
			});
			return {
				...message,
				role: "tool",
				input,
			};
		}
		return message;
	});
}