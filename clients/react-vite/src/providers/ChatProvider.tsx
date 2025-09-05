import { useContext, createContext } from "react";
import useChat from "@/hooks/useChat";
import useThread from "@/hooks/useThread";

export const ChatContext = createContext({});

export default function ChatProvider({children}: {children: React.ReactNode}) {
	const chatHooks = useChat();
	const threadHooks = useThread();
	return (
		<ChatContext.Provider value={{...chatHooks, ...threadHooks}}>
			{children}
		</ChatContext.Provider>
	);
}

export function useChatContext(): any {
	return useContext(ChatContext);
}
