import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
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
            <div className="w-full h-full overflow-y-auto p-4">
                {/* {JSON.stringify(messages, null, 2)} */}
                {messages.length > 0 &&
                    messages.map((message: any) => (
                        <div
                            key={message.id}
                            className="p-2 rounded-md bg-gray-100 my-2"
                        >
                            <h3 className="text-sm font-bold">
                                {message.role || message.type}{" "}
                                {message.type === "user" &&
                                    `[${message.model}]`}
                                {message.type === "tool" && `[${message.name}]`}
                            </h3>
                            <p>
                                {message.content ||
                                    JSON.stringify(message.input)}
                            </p>
                        </div>
                    ))}
            </div>
        </div>
    );
}

export default App;
