const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  CHAT: `${BACKEND_URL}/api/chat`,
  HEALTH: `${BACKEND_URL}/health`,
  MODELS: `${BACKEND_URL}/models`,
};

export const DEFAULT_MODEL = "meta/llama-3.3-70b-instruct";

export const SYSTEM_PROMPT = {
  role: "system",
  content:
    "You are a helpful, friendly AI assistant powered by NVIDIA NeMo. Provide clear, accurate, and concise responses.",
};
