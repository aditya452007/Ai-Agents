# AI Agents Repository

This repository showcases a variety of AI agent implementations, ranging from chat applications and RAG (Retrieval-Augmented Generation) pipelines to specialized MCP (Model Context Protocol) servers.

## Repository Structure

The repository is organized into the following main projects:

### 1. Av-Chatfriends
A ChatGPT-like web application that runs locally using `llama.cpp` and `flask`. It provides a web interface for interacting with local LLMs.

*   **Path:** `Av-Chatfriends/`
*   **Key Features:**
    *   Flask-based backend.
    *   OpenAI-compatible API integration (targeting local `llama.cpp`).
    *   Simple HTML/JS frontend.
    *   Docker support.
*   **Setup:** See [Av-Chatfriends/README.md](Av-Chatfriends/README.md) for details.

### 2. MCP (Model Context Protocol) Servers
This directory contains implementations of MCP servers, which allow AI models to interact with local resources.

*   **Path:** `MCP/`
*   **Sub-projects:**
    *   **File System Management MCP:** A server that provides full CRUD capabilities for file system operations.
        *   Path: `MCP/File_System_Management_MCP/`
        *   Setup: See [MCP/File_System_Management_MCP/SETUP_INSTRUCTIONS.md](MCP/File_System_Management_MCP/SETUP_INSTRUCTIONS.md).
    *   **Terminal Execution MCP:** A server that enables command execution across various shells (CMD, PowerShell, WSL, Git Bash).
        *   Path: `MCP/Terminal_Execution_MCP/`
        *   Setup: See [MCP/Terminal_Execution_MCP/SETUP_INSTRUCTIONS.md](MCP/Terminal_Execution_MCP/SETUP_INSTRUCTIONS.md).

### 3. RAG (Retrieval-Augmented Generation)
Contains Jupyter notebooks demonstrating RAG pipelines for different data sources.

*   **Path:** `RAG/`
*   **Contents:**
    *   `RAG_For_Url.ipynb`: RAG pipeline for querying web content.
    *   `Rag_For_Pdf.ipynb`: RAG pipeline for querying PDF documents.
*   **Requirements:** See `RAG/requirements.txt`.

### 4. Google Adk
Demonstrates a customer support agent using Google's Agent Development Kit (ADK) and Gemini models.

*   **Path:** `Google Adk/`
*   **Contents:**
    *   `customer-support-agent.ipynb`: A comprehensive notebook implementing a support agent.
*   **Requirements:** See `Google Adk/requirements.txt`.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Explore a project:**
    Navigate to the project directory you are interested in and follow its specific `README.md` or `SETUP_INSTRUCTIONS.md`.

    *   For the Chat App: `cd Av-Chatfriends`
    *   For MCP Servers: `cd MCP`
    *   For RAG Notebooks: `cd RAG`

## Prerequisites

*   **Python 3.10+** is recommended for all projects.
*   **Docker** is optional but recommended for `Av-Chatfriends`.
*   **Jupyter Notebook/Lab** is required to run the notebooks in `RAG` and `Google Adk`.
*   **API Keys**: Some projects (like `Google Adk` or `RAG`) may require API keys (e.g., Google Gemini, OpenAI) to be set in environment variables or Colab secrets.

## Contributing

Contributions are welcome! Please ensure you:
1.  Follow the existing code style.
2.  Add docstrings to any new functions or classes.
3.  Update the READMEs if you introduce new features or requirements.

## License

[License Information Here]
