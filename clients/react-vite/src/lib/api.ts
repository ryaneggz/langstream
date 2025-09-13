import { type ThreadAction } from "@/hooks/useThread";
class ApiClient {	
	readonly apiUrl: string;

	constructor(apiUrl: string) {
		this.apiUrl = apiUrl;
	}

	async invoke(model: string, system: string, messages: any[]) {
		const response = await fetch(`${this.apiUrl}/llm/invoke`, {
			method: "POST",
			body: JSON.stringify({ model, system, messages }),
		});
		return response
	}

	async searchThreads(
		action: ThreadAction,
		metadata: {thread_id?: string, checkpoint_id?: string} = {},
		limit: number = 100,
		offset: number = 0,
	) {
		let payload;
		if (action === 'list_threads') {
			payload = {
				limit: limit,
				offset: offset,
				metadata: metadata,
			};
		} else if (action === 'list_checkpoints') {
			payload = {
				limit: limit,
				offset: offset,
				metadata: { thread_id: metadata.thread_id },
			};
		} else if (action === 'get_checkpoint') {
			payload = {
				limit: limit,
				offset: offset,
				metadata: { thread_id: metadata.thread_id, checkpoint_id: metadata.checkpoint_id },
			};
		}
		const response = await fetch(`${this.apiUrl}/threads/search`, {
			method: "POST",
			headers: {
					"Content-Type": "application/json",
			},
			body: JSON.stringify(payload),
		});
		const data = await response.json();

		if (action === "list_threads") {
				return data.threads;
		} else if (action === "list_checkpoints") {
				return data.checkpoints;
		} else if (action === "get_checkpoint") {
				return data.checkpoint;
		}
	}

	async deleteThread(thread_id: string) {
		const response = await fetch(`${this.apiUrl}/threads/${thread_id}`, {
			method: "DELETE",
		});
		if (!response.ok) {
			throw new Error(`Failed to delete thread: ${response.statusText}`);
		}
		return response.json();
	}
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const apiClient = new ApiClient(API_URL);
export default apiClient;