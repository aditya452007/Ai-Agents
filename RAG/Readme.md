
# 🧠 RAG Agents: Document & Web Intelligence

A high-performance implementation of **Retrieval-Augmented Generation (RAG)** pipelines powered by **Google Gemini** and **LangChain**. This project enables natural language interaction with both static PDF documents and dynamic web content.

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| **`Rag_For_Pdf.ipynb`** | A pipeline designed to ingest, chunk, and index **PDF documents**. It features optimized parsing (PyMuPDF) and vector search to answer queries based on specific file contents. |
| **`RAG_For_Url.ipynb`** | A web-aware agent that scrapes and indexes content from **URLs**. It allows users to "chat" with live websites, documentation, or articles. |

## 🚀 Tech Stack

* **LLM:** Google Gemini 2.5 Flash (optimized for speed & latency)
* **Orchestration:** LangChain
* **Vector Store:** FAISS / ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2` / `bge-m3`)
* **Parsing:** PyMuPDF (Fitz) & WebBaseLoader

## 🛠️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/aditya452007/rag-agents.git](https://github.com/aditya452007/rag-agents.git)
    cd rag-agents
    ```

2.  **Install Dependencies**
    The notebooks handle dependency installation, but the core requirements are:
    ```bash
    pip install langchain-google-genai langchain-community faiss-cpu pymupdf chromadb
    ```

3.  **API Keys**
    You will need a Google Gemini API key.
    * Get it from [Google AI Studio](https://aistudio.google.com/).
    * The notebooks are configured to accept the key securely via `userdata` (Colab) or environment variables.

## 📖 Usage

### PDF Agent (`Rag_For_Pdf.ipynb`)
1.  Upload your target PDF to the runtime environment.
2.  Update the `pdf_path` variable with your filename.
3.  Run the pipeline to ingest and index the document.
4.  Query the agent to extract specific information, summaries, or comparative analysis.

### URL Agent (`RAG_For_Url.ipynb`)
1.  Input the target URL(s) into the loader.
2.  The agent will scrape, clean, and chunk the web content.
3.  Ask questions directly related to the website's content.

## ⚡ Performance Note
These implementations prioritize **low-latency inference**. By using optimized embedding models (like `MiniLM`) and efficient vector stores (FAISS), these agents are designed to run effectively on standard CPU environments (e.g., Google Colab free tier) without requiring heavy GPU resources.

---
*Created by [Aaditya Thakur](https://github.com/aditya452007)*
