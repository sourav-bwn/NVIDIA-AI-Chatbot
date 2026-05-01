# NVIDIA AI Chatbot 🤖

A beautiful ChatGPT-like AI chatbot powered by **NVIDIA NeMo API** with a modern React frontend and Python/FastAPI backend.

![NVIDIA AI Chat](https://img.shields.io/badge/NVIDIA-NeMo-76B900?style=for-the-badge&logo=nvidia)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)

## ✨ Features

- 🎨 **Beautiful UI** - Modern dark theme with gradient accents
- 💬 **Real-time chat** - Conversational AI powered by Meta Llama 3.3
- 🚀 **Fast & responsive** - Async backend with smooth frontend
- 📱 **Mobile-friendly** - Fully responsive design
- 🔄 **Conversation history** - Maintains context across messages
- 💡 **Smart suggestions** - Quick-start conversation prompts
- 🐳 **Docker ready** - Easy local development with docker-compose

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           Frontend (React)          │
│   ┌──────────┬──────────────────┐   │
│   │ Chat UI  │  State Management│   │
│   └──────────┴──────────────────┘   │
└──────────────┬──────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────┐
│          Backend (FastAPI)          │
│   ┌──────────┬──────────────────┐   │
│   │ API Routes│ NVIDIA Client   │   │
│   └──────────┴──────────────────┘   │
└──────────────┬──────────────────────┘
               │ API Calls
               ▼
┌─────────────────────────────────────┐
│        NVIDIA NeMo API              │
│   (Meta Llama 3.3 70B Instruct)     │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- NVIDIA API key ([Get one here](https://build.nvidia.com/))

### 1. Get NVIDIA API Key

1. Go to [NVIDIA Build](https://build.nvidia.com/)
2. Sign up / Sign in
3. Generate an API key
4. Copy the API key

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your NVIDIA API key
# NVIDIA_API_KEY=your_api_key_here

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (optional - defaults to localhost:8000)
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env.local

# Start the app
npm start
```

Frontend will open at `http://localhost:3000`

### 4. Using Docker (Alternative)

```bash
# Create .env file in root directory
echo "NVIDIA_API_KEY=your_api_key_here" > .env

# Start with docker-compose
docker-compose up --build
```

## 📁 Project Structure

```
nvidia-chatbot/
├── frontend/                 # React application
│   ├── public/               # Static files
│   ├── src/
│   │   ├── components/       # UI components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── Message.jsx
│   │   │   └── InputBox.jsx
│   │   ├── hooks/            # Custom React hooks
│   │   │   └── useChat.js
│   │   ├── styles/           # CSS styles
│   │   └── config.js         # API configuration
│   ├── package.json
│   └── Dockerfile
├── backend/                  # FastAPI application
│   ├── app/
│   │   └── main.py           # Main API file
│   ├── requirements.txt
│   ├── .env.example          # Environment template
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions
├── docker-compose.yml        # Docker setup
└── README.md
```

## 🌐 Deployment

### Frontend (GitHub Pages)

1. Push to GitHub
2. Go to Settings > Pages
3. Select `gh-pages` branch
4. Set `REACT_APP_BACKEND_URL` in repository secrets

### Backend (Render/Railway)

#### Deploy to Render:

1. Connect your GitHub repo
2. Set build command: `pip install -r backend/requirements.txt`
3. Set start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Add `NVIDIA_API_KEY` as environment variable

#### Deploy to Railway:

1. Connect your GitHub repo
2. Add environment variable `NVIDIA_API_KEY`
3. Railway will auto-detect Python and deploy

### Configure Frontend After Backend Deployment

Update your frontend environment:

```bash
# In frontend/.env or GitHub repository secrets
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

## 🔧 API Endpoints

### Backend

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send chat message and get response |
| POST | `/api/chat/stream` | Stream chat responses |
| GET | `/health` | Health check |
| GET | `/models` | List available models |

### Request Format

```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "model": "meta/llama-3.3-70b-instruct",
  "temperature": 0.7,
  "max_tokens": 1024
}
```

### Response Format

```json
{
  "content": "Hello! How can I help you today?",
  "model": "meta/llama-3.3-70b-instruct",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

## 🎨 Customization

### Change the Model

Edit `backend/.env`:

```env
MODEL_NAME=meta/llama-3.1-8b-instruct
```

Available models:
- `meta/llama-3.3-70b-instruct` (default)
- `meta/llama-3.1-8b-instruct`
- `mistralai/mixtral-8x7b-instruct-v0.1`
- `google/gemma-7b`

### Change Theme Colors

Edit `frontend/src/components/ChatInterface.css`:

```css
/* Change gradient colors */
.chat-header {
  background: linear-gradient(135deg, #your-color 0%, #your-color 100%);
}
```

### Change System Prompt

Edit `frontend/src/config.js`:

```javascript
export const SYSTEM_PROMPT = {
  role: "system",
  content: "Your custom system prompt here",
};
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [NVIDIA Build](https://build.nvidia.com/) - Get API key
- [NVIDIA NeMo Docs](https://docs.nvidia.com/nemo-framework/) - Documentation
- [Meta Llama](https://ai.meta.com/llama/) - Model information

---

Built with ❤️ using NVIDIA NeMo API
