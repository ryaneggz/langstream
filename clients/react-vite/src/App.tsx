import { SSE } from "sse.js";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { useChatContext } from "@/providers/chat-provider";

const in_mem_messages: any[] = [];

function App() {
    const [query, setQuery] = useState("");
    const { sseHandler, clearContent, messages } = useChatContext();

    const handleSubmit = () => {
        console.log("Submitted:", query);
        handleSSE(query);
        setQuery("");
    };

    const handleSSE = (query: string) => {
        clearContent();
        const options = {
            // autoReconnect: true,
            // reconnectDelay: 3000,
            // maxRetries: 3,
            // useLastEventId: true,
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "text/event-stream",
            },
            payload: JSON.stringify({
                model: "openai:gpt-5-nano",
                stream_mode: "messages",
                system: "You are a helpful assistant.",
                messages: [{ role: "user", content: query }],
            }),
        };
        var source = new SSE("http://localhost:8000/llm/stream", options);
        source.addEventListener("message", function (e: any) {
            // Assuming we receive JSON-encoded data payloads:
            let payload = JSON.parse(e.data);
            sseHandler(payload, in_mem_messages, "messages");
        });

        source.addEventListener("error", (e: any) => {
            console.error("Error:", e);
        });
    };

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
                {messages.length > 0 && messages.map((message: any) => (
                    <div key={message.id} className="p-2 rounded-md bg-gray-100 my-2">
                        <h3 className="text-sm font-bold">{message.type}</h3>
                        <p>{message.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
