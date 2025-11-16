# AV ChatFriends - AI Chat Application

A ChatGPT-like web interface for interacting with a local AI model (llama.cpp) via an OpenAI-compatible API.

## 👥 Project Team

**Frontend Development:** Vishal Koushal  
**Backend & Architecture:** Aaditya Thakur

---

## 🚀 Features

- 🤖 **ChatGPT-like web interface** with modern, responsive UI
- 🔌 **Local llama.cpp integration** via OpenAI-compatible API
- 🐳 **Docker support** for containerized deployment
- 📝 **Comprehensive error handling** and edge case testing
- 🎨 **Modern UI/UX** with dark theme and smooth animations
- ⚡ **Real-time chat responses** with loading indicators
- 💚 **Health monitoring** with status indicators

---

## 📋 Requirements

- **Python:** 3.13+
- **Local llama.cpp server:** Running on port 12434
- **Model:** `ai/smollm2` (or configure your own model)

---

## 🛠️ Installation

### 1. Clone or navigate to the project directory

```bash
cd Av-Chatfriends
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with the following variables:

```env
BASE_URL=http://localhost:12434/engines/llama.cpp/v1
MODEL_NAME=ai/smollm2
API_KEY=not-needed
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
MAX_TOKENS=500
TEMPERATURE=0.7
```

### 4. Ensure your llama.cpp server is running

Make sure you have a local llama.cpp server running on `localhost:12434` with the model `ai/smollm2` loaded.

---

## 🎯 Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`. Open your browser and navigate to this URL to access the chat interface.

---

## 📡 API Endpoints

### POST `/api/chat`

Send a chat message and receive a response.

**Request:**
```json
{
    "prompt": "Hello, how are you?",
    "model": "ai/smollm2",
    "max_tokens": 500,
    "temperature": 0.7
}
```

**Response:**
```json
{
    "success": true,
    "message": "I'm doing well, thank you for asking!",
    "model": "ai/smollm2"
}
```

### GET `/api/health`

Check the health status of the server and model connection.

---

## 🐳 Docker Usage

### Build the Docker image

```bash
docker build -t av-chatfriends .
```

### Run the container

```bash
docker run -p 5000:5000 --env-file .env av-chatfriends
```

---

## 📁 Project Structure

```
Av-Chatfriends/
├── app.py              # Main Flask application with API endpoints
├── index.html          # ChatGPT-like web interface (by Vishal Koushal)
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

---

## ⚙️ Configuration

### Environment Variables

- **BASE_URL:** Base URL for the OpenAI-compatible API
- **MODEL_NAME:** Name of the model to use
- **API_KEY:** API key for authentication
- **FLASK_HOST:** Flask server host
- **FLASK_PORT:** Flask server port
- **FLASK_DEBUG:** Enable Flask debug mode
- **MAX_TOKENS:** Maximum tokens to generate
- **TEMPERATURE:** Temperature for response generation

---

## 🛡️ Edge Cases Handled

The application includes comprehensive error handling for:

- Empty prompts
- Connection errors (server not running)
- API errors and timeouts
- Invalid responses
- Missing configuration
- Client initialization failures

---

## 🔧 Troubleshooting

### Server not connecting

1. Ensure your llama.cpp server is running on port 12434
2. Check that the `BASE_URL` in `.env` is correct
3. Verify the model name matches your server's model

### Port already in use

Change the `FLASK_PORT` in your `.env` file to a different port (e.g., `5001`)

---

## 📄 License

This project is open source and available for personal and commercial use.

---

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

## 👨‍💻 Credits

- **Frontend Design & Development:** Vishal Koushal
- **Backend Architecture, API Integration & DevOps:** Aaditya Thakur

---

**Built with ❤️ using Flask, Python, and Modern Web Technologies**
