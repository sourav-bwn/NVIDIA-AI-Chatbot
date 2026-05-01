import { useState, useCallback } from "react";
import axios from "axios";
import { API_ENDPOINTS, SYSTEM_PROMPT, DEFAULT_MODEL } from "../config.js";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [streaming, setStreaming] = useState(false);

  const sendMessage = useCallback(
    async (userMessage) => {
      if (!userMessage.trim() || isLoading) return;

      const newMessages = [...messages, { role: "user", content: userMessage }];
      setMessages(newMessages);
      setIsLoading(true);
      setError(null);

      try {
        const apiMessages = [SYSTEM_PROMPT, ...newMessages];

        const response = await axios.post(API_ENDPOINTS.CHAT, {
          messages: apiMessages,
          model: DEFAULT_MODEL,
        });

        const assistantMessage = {
          role: "assistant",
          content: response.data.content,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const errorMessage =
          err.response?.data?.detail ||
          err.message ||
          "Failed to get response. Please try again.";
        setError(errorMessage);

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `⚠️ Error: ${errorMessage}`,
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [messages, isLoading]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearChat,
  };
}
