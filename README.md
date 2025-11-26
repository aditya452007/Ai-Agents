# AI Agents Showcase: A Diverse Collection of Intelligent Systems

This repository serves as a showcase for a variety of AI agents, each demonstrating unique capabilities and leveraging different technologies. From conversational AI to Retrieval-Augmented Generation (RAG) and customer support automation, these projects highlight the diverse possibilities of modern AI development.

## 🚀 Agents Overview

This collection features three distinct AI agent implementations:

1.  **Av-Chatfriends:** A real-time, ChatGPT-like web application.
2.  **RAG Agents:** High-performance RAG pipelines for interacting with documents and websites.
3.  **Google Adk Customer Support Agent:** An advanced customer support agent built with Google's Agent Development Kit.

---

### 1. Av-Chatfriends

**[➡️ View Code](./Av-Chatfriends)**

A ChatGPT-like web interface for interacting with a local AI model via an OpenAI-compatible API. This project demonstrates a complete, containerized web application for real-time conversational AI.

**Key Features:**
- **Real-time Chat Interface:** Modern, responsive UI for seamless interaction.
- **Local Model Integration:** Connects to a local Docker Model runner.
- **Docker Support:** Fully containerized for easy deployment.
- **Health Monitoring:** Includes an API endpoint for system health checks.

**Technologies Used:**
- **Backend:** Flask, Python
- **Frontend:** HTML, JavaScript
- **Deployment:** Docker

---

### 2. RAG Agents: Document & Web Intelligence

**[➡️ View Code](./RAG)**

A high-performance implementation of **Retrieval-Augmented Generation (RAG)** pipelines powered by **Google Gemini** and **LangChain**. This project enables natural language interaction with both static PDF documents and dynamic web content.

**Key Features:**
- **PDF Document Agent:** Ingests, chunks, and indexes PDF documents for querying.
- **Web URL Agent:** Scrapes and indexes content from URLs to "chat" with live websites.
- **Optimized Performance:** Designed for low-latency inference on standard CPU environments.

**Technologies Used:**
- **LLM:** Google Gemini
- **Orchestration:** LangChain
- **Vector Store:** FAISS / ChromaDB
- **Embeddings:** HuggingFace

---

### 3. Google Adk Customer Support Agent

**[➡️ View Code](./Google%20Adk)**

An advanced, multi-tool customer support agent built using **Google's Agent Development Kit (ADK)**. This agent demonstrates how to create a sophisticated system that can interact with multiple external tools to provide comprehensive customer support.

**Key Features:**
- **Multi-Agent System:** Composed of specialized sub-agents for product information, inventory, and shipping.
- **Tool Integration:** Leverages multiple tools to fetch and synthesize information from different sources.
- **A2A Communication:** Utilizes the Agent-to-Agent (A2A) communication protocol.
- **Scalable Architecture:** Built to be extensible and scalable for real-world applications.

**Technologies Used:**
- **Framework:** Google Agent Development Kit (ADK)
- **Model:** Google Gemini
- **Deployment:** Uvicorn, FastAPI

---

## 🛠️ Getting Started

Each agent is contained within its own directory and has its own set of instructions and dependencies. To get started with a specific agent, please navigate to its directory and consult the `README.md` file within it.

- **[Av-Chatfriends Instructions](./Av-Chatfriends/README.md)**
- **[RAG Agents Instructions](./RAG/README.md)**
- **[Google Adk Customer Support Agent](./Google%20Adk/customer-support-agent.ipynb)**

## 🤝 Contributing

Contributions are welcome! If you have an idea for a new agent, an improvement to an existing one, or a bug fix, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or fix.
3.  **Submit a pull request** with a clear description of your changes.

## 📧 Contact

For any inquiries or collaboration opportunities, please feel free to contact the repository owner. We are always open to discussing new ideas and projects.
