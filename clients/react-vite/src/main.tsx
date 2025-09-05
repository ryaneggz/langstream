import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import ChatProvider from "./providers/ChatProvider.tsx";

createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<ChatProvider>
			<App />
		</ChatProvider>
	</StrictMode>
);
