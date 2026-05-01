import React from "react";
import { ChatInterface } from "./components/ChatInterface.jsx";
import { useChat } from "./hooks/useChat.js";
import "./styles/App.css";

function App() {
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  return (
    <div className="app">
      <ChatInterface
        messages={messages}
        onSend={sendMessage}
        isLoading={isLoading}
        onClear={clearChat}
      />
      {error && <div className="error-toast">{error}</div>}
    </div>
  );
}

export default App;
