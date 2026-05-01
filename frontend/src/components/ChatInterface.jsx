import React, { useEffect, useRef } from "react";
import { Message } from "./Message";
import { InputBox } from "./InputBox";
import "./ChatInterface.css";

export function ChatInterface({ messages, onSend, isLoading, onClear }) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div className="header-content">
          <div className="header-title">
            <span className="nvidia-logo">🟢</span>
            <h1>NVIDIA AI Chat</h1>
          </div>
          <div className="header-actions">
            <button className="clear-button" onClick={onClear}>
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M3 6h18" />
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
              </svg>
              Clear Chat
            </button>
          </div>
        </div>
      </header>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-screen">
            <div className="welcome-icon">🤖</div>
            <h2>Welcome to NVIDIA AI Chat</h2>
            <p>Powered by NVIDIA NeMo • Meta Llama 3.3</p>
            <div className="suggestions">
              <button
                className="suggestion"
                onClick={() => onSend("Explain quantum computing in simple terms")}
              >
                Explain quantum computing
              </button>
              <button
                className="suggestion"
                onClick={() => onSend("Write a Python function to sort a list")}
              >
                Write a Python sorting function
              </button>
              <button
                className="suggestion"
                onClick={() => onSend("What are the latest trends in AI?")}
              >
                Latest AI trends
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, index) => (
              <Message key={index} message={msg} />
            ))}
            {isLoading && (
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputBox onSend={onSend} isLoading={isLoading} />
    </div>
  );
}
