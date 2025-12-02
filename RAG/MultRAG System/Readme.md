# MultiRAG System (Neural Nexus)

A unified, advanced Retrieval-Augmented Generation (RAG) system capable of ingesting knowledge from both **PDF documents** and **Live Websites**. It features a high-performance FastAPI backend running inside a Jupyter Notebook and a futuristic "Neural Nexus" frontend interface.

## 🌟 Features

*   **Dual-Source Ingestion:**
    *   **Files:** Drag-and-drop support for PDF, MD, and TXT files (with corruption handling).
    *   **Web:** Live URL crawling and scraping with depth control and content cleaning.
*   **Advanced RAG Pipeline:**
    *   **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (Local CPU optimized).
    *   **Indexing:** FAISS (Facebook AI Similarity Search) with Inner Product metric for speed.
    *   **LLM:** Google Gemini 2.5 Flash for high-speed, accurate generation.
*   **Robust Backend:** FastAPI server running asynchronously within a Jupyter environment.
*   **Modern Frontend (Neural Nexus):**
    *   Glassmorphism UI design with ambient animations.
    *   Real-time processing feedback (Terminal style).
    *   Markdown rendering and syntax highlighting for code blocks.
    *   "Memory Purge" functionality to reset the session and free up RAM/VRAM.

## 🛠️ Technical Stack

*   **Backend:** Python 3.10+, FastAPI, Uvicorn, LangChain, PyMuPDF (Fitz), BeautifulSoup4, FAISS, Google Generative AI.
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, GSAP (Animations), Marked.js, Highlight.js, Phosphor Icons.

## 🚀 Setup & Usage

### 1. Prerequisites
*   Python 3.10 or higher.
*   Jupyter Notebook environment (Local or Google Colab).
*   A Google Gemini API Key.

### 2. Installation
Ensure you have the required Python libraries. You can run the first cell in the notebook or install them via pip:

```bash
pip install fastapi uvicorn python-multipart nest-asyncio langchain-google-genai langchain-community langchain-text-splitters langchain-core sentence-transformers faiss-cpu pymupdf requests beautifulsoup4 numpy torch python-dotenv
```

### 3. Configuration
*   **API Key:** The system requires a `GEMINI_API_KEY`.
    *   **Option A:** Create a `.env` file in this directory with `GEMINI_API_KEY=your_key_here`.
    *   **Option B:** The notebook is set to load from `.env`, but you can also manually input it in the "Load Embedding Model & GEMINI_API_KEY" cell if running in Colab secrets.

### 4. Running the System

**Step 1: Start the Backend**
1.  Open `Multi_Rag.ipynb` in your Jupyter environment.
2.  Run all cells.
3.  Wait for the final cell to output: `🚀 Server starting at http://127.0.0.1:8000`.

**Step 2: Launch the Frontend**
1.  Locate `index.html` in this folder.
2.  Open it directly in your web browser.
3.  *Note:* The backend is configured with CORS to allow connections from local HTML files.

### 5. Using the Interface

1.  **Ingestion Phase:**
    *   **For Files:** Drag & drop a PDF into the card.
    *   **For Web:** Paste a URL and click the arrow button.
    *   The system will process the data and build the vector index.
2.  **Synapse Phase (Chat):**
    *   Once indexed, the chat interface appears.
    *   Ask questions about the uploaded content.
    *   The "Thinking..." indicator shows when the RAG pipeline is retrieving context and generating an answer.
3.  **Reset:**
    *   Click "Purge Memory" to clear the vector store and restart the session.

## 📜 License

This project is open-source and available under the MIT License.
