import React from "react";
import "./Message.css";

export function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message ${isUser ? "user-message" : "ai-message"}`}>
      <div className={`message-avatar ${isUser ? "user-avatar" : "ai-avatar"}`}>
        {isUser ? "👤" : "🤖"}
      </div>
      <div className={`message-content ${isUser ? "user-bubble" : "ai-bubble"}`}>
        <div className="message-text">{message.content}</div>
        <div className="message-time">
          {message.timestamp?.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  );
}
