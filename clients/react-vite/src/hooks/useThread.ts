
import { useEffect, useState } from 'react';
import apiClient from '@/lib/api';

export type ThreadContextType = {
	threads: any[];
	setThreads: (threads: any[]) => void;
	checkpoints: any[];
	setCheckpoints: (checkpoints: any[]) => void;
	checkpoint: any;
	setCheckpoint: (checkpoint: any) => void;
	searchThreads: (action: 'list_threads' | 'list_checkpoints' | 'get_checkpoint', metadata: {thread_id?: string, checkpoint_id?: string}) => void;
	useListThreadsEffect: (trigger?: boolean) => void;
};

export default function useThread(): ThreadContextType {
	const [threads, setThreads] = useState<any[]>([]);
	const [checkpoints, setCheckpoints] = useState<any[]>([]);
	const [checkpoint, setCheckpoint] = useState<any>(null);

	const searchThreads = async (
		action: 'list_threads' | 'list_checkpoints' | 'get_checkpoint',
		metadata: {thread_id?: string, checkpoint_id?: string} = {}
	) => {
		const data = await apiClient.searchThreads(action, metadata);
		
		if (action === 'list_threads') {
			setThreads(data);
		} else if (action === 'list_checkpoints') {
			setCheckpoints(data);
		} else if (action === 'get_checkpoint') {
			setCheckpoint(data);
		}
	};

	const useListThreadsEffect = (trigger?: boolean) => {
		useEffect(() => {
			searchThreads('list_threads');
		}, [,trigger]);
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
