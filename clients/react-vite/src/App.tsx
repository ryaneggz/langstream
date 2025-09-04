import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useChatContext } from "@/providers/ChatProvider";
import { type ChatContextType } from "@/hooks/useChat";

function App() {
    const { query, setQuery, handleSubmit, messages } =
        useChatContext() as ChatContextType;

    return (
        <div className="fixed inset-0 flex flex-col w-full h-full">
            <div className="p-4 border-b space-y-2">
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
            <div className="flex-1 flex flex-col overflow-hidden">
                <Tabs defaultValue="messages" className="flex-1 flex flex-col">
                    <div className="p-4 pb-0">
                        <TabsList>
                            <TabsTrigger value="messages">Messages</TabsTrigger>
                            <TabsTrigger value="threads">Threads</TabsTrigger>
                            <TabsTrigger value="tools">Tools</TabsTrigger>
                            <TabsTrigger value="settings">Settings</TabsTrigger>
                        </TabsList>
                    </div>
                    <TabsContent
                        value="messages"
                        className="flex-1 overflow-y-auto p-4 pt-0"
                    >
                        {messages.length > 0 ? (
                            messages.map((message: any) => (
                                <div
                                    key={message.id}
                                    className="p-2 rounded-md bg-gray-100 my-2"
                                >
                                    <h3 className="text-sm font-bold">
                                        {message.role || message.type}{" "}
                                        {message.type === "user" &&
                                            `[${message.model}]`}
                                        {message.type === "tool" &&
                                            `[${message.name}]`}
                                    </h3>
                                    <p>
                                        {message.content ||
                                            JSON.stringify(message.input)}
                                    </p>
                                </div>
                            ))
                        ) : (
                            <div className="pt-4">
                                <div className="text-center text-muted-foreground">
                                    <p>No messages yet</p>
                                    <p className="text-sm mt-2">
                                        Start a conversation by typing in the input field above.
                                    </p>
                                </div>
                            </div>
                        )}
                    </TabsContent>
                    <TabsContent
                        value="threads"
                        className="flex-1 overflow-y-auto p-4 pt-0"
                    >
                        <div className="pt-4">
                            <div className="text-center text-muted-foreground">
                                <p>Threads feature coming soon...</p>
                                <p className="text-sm mt-2">
                                    This will show conversation threads and chat
                                    history.
                                </p>
                            </div>
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
                        <div className="pt-4">
                            <div className="text-center text-muted-foreground">
                                <p>Settings feature coming soon...</p>
                                <p className="text-sm mt-2">
                                    This will show available settings and their
                                    descriptions.
                                </p>
                            </div>
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}

export default App;
