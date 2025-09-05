
import { useEffect, useState } from 'react';

export type ThreadContextType = {
	threads: any[];
	setThreads: (threads: any[]) => void;
	checkpoints: any[];
	setCheckpoints: (checkpoints: any[]) => void;
	checkpoint: any;
	setCheckpoint: (checkpoint: any) => void;
	searchThreads: (action: string, metadata: {thread_id?: string, checkpoint_id?: string}) => void;
	useListThreadsEffect: () => void;
};

export default function useThread(): ThreadContextType {
	const [threads, setThreads] = useState<any[]>([]);
	const [checkpoints, setCheckpoints] = useState<any[]>([]);
	const [checkpoint, setCheckpoint] = useState<any>(null);

	const searchThreads = async (
		action: string,
		metadata: {thread_id?: string, checkpoint_id?: string} = {}
	) => {
		let payload;
		if (action === 'list_threads') {
			payload = {
				limit: 10,
				offset: 0,
				metadata: metadata,
			};
		} else if (action === 'list_checkpoints') {
			payload = {
				limit: 10,
				offset: 0,
				metadata: { thread_id: metadata.thread_id },
			};
		} else if (action === 'get_checkpoint') {
			payload = {
				limit: 10,
				offset: 0,
				metadata: { thread_id: metadata.thread_id, checkpoint_id: metadata.checkpoint_id },
			};
		}
		
		const response = await fetch('http://localhost:8000/threads/search', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		});
		const data = await response.json();
		
		if (action === 'list_threads') {
			setThreads(data.threads);
		} else if (action === 'list_checkpoints') {
			setCheckpoints(data.checkpoints);
		} else if (action === 'get_checkpoint') {
			setCheckpoint(data.checkpoint);
		}
	};

	const useListThreadsEffect = () => {
		useEffect(() => {
			searchThreads('list_threads');
		}, []);
	};

	return {
		threads,
		setThreads,
		checkpoints,
		setCheckpoints,
		checkpoint,
		setCheckpoint,
		searchThreads,
		useListThreadsEffect,
	};
}
