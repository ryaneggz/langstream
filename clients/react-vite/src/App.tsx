import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useChatContext } from "@/providers/ChatProvider";
import { type ChatContextType } from "@/hooks/useChat";
import { type ThreadContextType } from "@/hooks/useThread";
import { formatMessages } from "./lib/utils";

function App() {
	const { useListThreadsEffect, threads, checkpoint } = useChatContext() as ThreadContextType;	
	const { query, setQuery, handleSubmit, messages, setMessages, metadata, setMetadata } =
		useChatContext() as ChatContextType;
	const [currentTab, setCurrentTab] = useState("messages");
	const bottomRef = useRef<HTMLDivElement>(null);

	// Set current tab to messages when query changes
	useEffect(() => {
		setCurrentTab("messages");
	}, [query]);

	// Fetch threads when current tab is threads
	useListThreadsEffect(currentTab === "threads");

	// Scroll to bottom of messages when messages change
	useEffect(() => {
		bottomRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages]);

	// Set messages when checkpoint changes
	useEffect(() => {
		if (checkpoint && checkpoint.channel_values) {
			setMessages(checkpoint.channel_values.messages);
		}
	}, [checkpoint]);

	return (
		<div className="flex flex-col w-full h-screen">
			<div className="flex-1 flex flex-col">
				<Tabs value={currentTab} onValueChange={setCurrentTab} className="flex-1 flex flex-col">
					<div className="p-4 pb-0">
						<TabsList>
							<TabsTrigger className="cursor-pointer" value="messages">Messages</TabsTrigger>
							<TabsTrigger className="cursor-pointer" value="threads">Threads</TabsTrigger>
							<TabsTrigger className="cursor-pointer" value="tools">Tools</TabsTrigger>
							<TabsTrigger className="cursor-pointer" value="settings">Settings</TabsTrigger>
						</TabsList>
					</div>
					<TabsContent
						value="messages"
						className="flex-1 p-4 pt-0 flex flex-col overflow-hidden max-h-[calc(100vh-150px)]"
					>
						<ScrollArea className="flex-1 whitespace-pre-wrap h-0">
							{messages.length > 0 ? (
								messages.map((message: any) => (
									<div
										key={message.id}
										className="p-2 rounded-md bg-gray-100 my-2"
									>
										<h3 className="text-sm font-bold">
											{message.role || message.type}{" "}
											{message.type === "user" && `[${message.model}]`}
											{message.type === "tool" && `[${message.name}]`}
										</h3>
										<p>{message.content || JSON.stringify(message.input)}</p>
									</div>
								))
							) : (
								<div className="pt-4 text-center text-muted-foreground">
									<p>No messages yet</p>
									<p className="text-sm mt-2">
										Start a conversation by typing in the input field above.
									</p>
								</div>
							)}
							<div ref={bottomRef} />
						</ScrollArea>
					</TabsContent>
					<TabsContent
						value="threads"
						className="flex-1 overflow-y-auto p-4 pt-0"
					>
						<div className="pt-4">
							{threads.length > 0 ? (
								<div className="space-y-2">
									{threads.map((thread: any, index: number) => (
										<div
											key={thread.thread_id || index}
											className="p-3 rounded-md bg-gray-100 border cursor-pointer"
											onClick={() => {
												setMessages(formatMessages(thread.checkpoint.channel_values.messages))
												setMetadata(JSON.stringify({ thread_id: thread.thread_id}))
												setCurrentTab("messages");
											}}
										>
											<div className="flex justify-between items-start">
												<div className="flex-1">
													<h4 className="text-sm font-medium">
														{thread.thread_id}
													</h4>
													{thread.updated_at && (
														<p className="text-xs text-gray-500 mt-1">
															Updated: {new Date(thread.updated_at).toLocaleString()}
														</p>
													)}
												</div>
											</div>
											{thread.metadata && (
												<div className="mt-2">
													<pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
														{JSON.stringify(thread.metadata, null, 2)}
													</pre>
												</div>
											)}
										</div>
									))}
								</div>
							) : (
								<div className="text-center text-muted-foreground">
									<p>No threads found</p>
									<p className="text-sm mt-2">
										Start a conversation to create your first thread.
									</p>
								</div>
							)}
						</div>
					</TabsContent>
					<TabsContent
						value="tools"
						className="flex-1 overflow-y-auto p-4 pt-0"
					>
						<div className="pt-4">
							<div className="text-center text-muted-foreground">
								<p>Tools feature coming soon...</p>
								<p className="text-sm mt-2">
										This will show available tools and their
										descriptions.
								</p>
							</div>
						</div>
					</TabsContent>
					<TabsContent
						value="settings"
						className="flex-1 overflow-y-auto p-4 pt-0"
					>
						<div className="pt-4 space-y-4">
							<div>
								<label className="text-sm font-medium mb-2 block">
									Metadata (JSON)
								</label>
								<Textarea
									placeholder='{"key": "value"}'
									className="min-h-32 font-mono text-sm"
									value={metadata}
									onChange={(e) => setMetadata(e.target.value)}
								/>
							</div>
						</div>
					</TabsContent>
				</Tabs>
			</div>
			<div className="p-4 border-t space-y-2">
				<Textarea
					placeholder="Enter your query..."
					className="w-full resize-none"
					value={query}
					onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
						setQuery(e.target.value)
					}
					onKeyDown={(
						e: React.KeyboardEvent<HTMLTextAreaElement>
					) => {
						if (e.key === "Enter" && !e.shiftKey) {
							e.preventDefault();
							handleSubmit();
						}
					}}
				/>
				<Button onClick={handleSubmit} className="w-full">
					Submit
				</Button>
			</div>
		</div>
	);
}

export default App;
