# 🤖 AI Agents - Model Context Protocol (MCP) Servers

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Enabled-green)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Overview

This directory contains a collection of powerful **Model Context Protocol (MCP)** servers built with Python. These servers are designed to bridge the gap between Large Language Models (LLMs) and your local operating system, granting AI agents the agency to perform real-world tasks.

By integrating these servers with an MCP-compliant client (such as Claude Desktop), you empower AI to:

1.  **Manage the File System:** Read, write, organize, and analyze files directly on the host machine.
2.  **Execute Terminal Commands:** Run shell commands, manage processes, and automate system tasks via Bash, PowerShell, or CMD.

> **⚠️ SECURITY WARNING**: These tools grant an AI agent significant access to your operating system. It is highly recommended to run these servers in a sandboxed environment (e.g., Docker container, Virtual Machine) or strictly monitor their usage.

---

## 🛠️ Available MCP Servers

### 1. File System Management MCP
**Directory:** `/filesystem_mcp` (Adjust based on your actual folder name)

This server provides tools that allow the AI to interact with the OS file system. It acts as a bridge for file I/O operations, enabling the AI to act as an automated developer or system administrator.

**Capabilities:**
* **Read/Write Files:** Create new files, read content, and edit existing files.
* **Directory Management:** Create directories, list folder contents, and navigate the tree structure.
* **File Operations:** Move, copy, rename, and delete files securely.
* **Metadata:** Retrieve file information (size, creation date, permissions).

**Ideal Use Cases:**
* Automated code refactoring across multiple files.
* Log file analysis and summarization.
* Organizing cluttered directories based on file types.

### 2. Terminal Execution MCP
**Directory:** `/terminal_mcp` (Adjust based on your actual folder name)

This server exposes a terminal interface to the AI, allowing it to execute system commands. It supports various shell environments depending on the host OS.

**Capabilities:**
* **Command Execution:** Run commands in `bash`, `zsh`, `cmd`, or `powershell`.
* **Output Retrieval:** Capture `stdout` and `stderr` to analyze command results.
* **Chain Commands:** Execute complex sequences of commands (e.g., git workflows, build scripts).

**Ideal Use Cases:**
* Environment setup and dependency installation.
* Git automation (cloning, committing, pushing).
* System diagnostics and network troubleshooting.

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+** installed on your system.
* An MCP-compliant client (e.g., [Claude Desktop App](https://claude.ai/download)).

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/aditya452007/Ai-Agents.git](https://github.com/aditya452007/Ai-Agents.git)
    cd Ai-Agents/MCP
    ```

2.  **Set Up a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Make sure you have the `mcp` python SDK and any other required libraries.
    ```bash
    pip install mcp
    # If you have a requirements.txt file:
    # pip install -r requirements.txt
    ```

---

## ⚙️ Configuration

To use these servers with **Claude Desktop**, you need to update your configuration file.

**Config Location:**
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the following entries to the `mcpServers` object. **Note:** You must replace `/absolute/path/to/...` with the actual absolute paths on your machine.

```json
{
  "mcpServers": {
    "filesystem-mcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/Ai-Agents/MCP/filesystem_server.py"
      ]
    },
    "terminal-mcp": {
      "command": "python",
      "args": [
        "/absolute/path/to/Ai-Agents/MCP/terminal_server.py"
      ]
    }
  }
}
```
---
## 🛡️ Safety & Security Guidelines

Giving an AI access to your terminal and file system is powerful but carries risks. Please adhere to these guidelines:

Allowed Directories: Modify the File System MCP code to restrict access to specific directories (e.g., only allow access to a /workspace folder) to prevent accidental modification of system files.

Human in the Loop: Always review the commands or file changes the AI proposes before confirming execution, especially for destructive actions like rm or delete.

Sandboxing: For maximum security, run these MCP servers inside a Docker container.
---
## 🤝 Contributing

Contributions are welcome! If you have ideas for new tools (e.g., Git control, Browser automation) or improvements to the existing ones:

Fork the repository.

Create a feature branch (git checkout -b feature/AmazingFeature).

Commit your changes.

Push to the branch.

Open a Pull Request.
---
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
