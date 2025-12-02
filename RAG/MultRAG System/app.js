/* MultiRAG Frontend Logic V2
   Author: Senior Frontend Architect
   Features: GSAP Animations, Markdown, Glass UI
*/

// --- CONFIG ---
const API_BASE = 'http://127.0.0.1:8000'; 

// --- STATE ---
const store = {
    currentFile: null,
    fileSize: null,
    sessionId: null,
    isProcessing: false
};

// --- DOM ELEMENTS ---
const elements = {
    viewIngestion: document.getElementById('view-ingestion'),
    viewSynapse: document.getElementById('view-synapse'),
    
    // Ingestion
    dropZone: document.getElementById('drop-zone'),
    fileInput: document.getElementById('file-input'),
    urlInput: document.getElementById('url-input'),
    scrapeBtn: document.getElementById('scrape-btn'),
    processingOverlay: document.getElementById('processing-overlay'),
    termText: document.getElementById('terminal-text'),
    
    // Synapse
    metaFilename: document.getElementById('meta-filename'),
    metaSize: document.getElementById('meta-size'),
    metaTokens: document.getElementById('meta-tokens'),
    chatIntroFilename: document.getElementById('chat-intro-filename'),
    chatStream: document.getElementById('chat-stream'),
    chatInput: document.getElementById('chat-input'),
    sendBtn: document.getElementById('send-btn'),
    resetBtn: document.getElementById('reset-session')
};

// --- INITIAL ANIMATIONS ---
document.addEventListener('DOMContentLoaded', () => {
    // Entrance Animation for Ingestion Hub
    gsap.from(".hub-card", {
        duration: 1,
        y: 30,
        opacity: 0,
        ease: "power3.out"
    });
});

// --- NETWORK LAYER ---
async function sendRequest(endpoint, data, type = 'json') {
    const options = { method: 'POST' };

    if (type === 'file' || type === 'form') {
        const formData = new FormData();
        for (const key in data) formData.append(key, data[key]);
        options.body = formData;
    } else {
        options.headers = { 'Content-Type': 'application/json' };
        options.body = JSON.stringify(data);
    }

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Server Error: ${res.status}`);
        }
        return await res.json();
    } catch (err) {
        console.error(`Req Failed [${endpoint}]:`, err);
        throw err;
    }
}

// --- LOGIC FLOWS ---

// 1. INGESTION
async function handleIngestion(sourceType, payload) {
    if (store.isProcessing) return;
    store.isProcessing = true;
    
    // Show Overlay
    elements.processingOverlay.classList.remove('hidden');
    gsap.fromTo(".loader-content", {opacity: 0}, {opacity: 1, duration: 0.5});
    
    elements.termText.innerText = sourceType === 'file' ? "Extracting Vectors..." : "Crawling Neural Web...";

    try {
        let response;
        if (sourceType === 'file') {
            response = await sendRequest('/upload', { file: payload }, 'file');
            store.fileSize = (payload.size / 1024 / 1024).toFixed(2) + " MB";
            store.currentFile = payload.name;
        } else {
            response = await sendRequest('/scrape', { url: payload }, 'form');
            store.fileSize = "Web Node";
            store.currentFile = payload;
        }

        store.sessionId = response.session_id;
        
        // Success Transition
        setTimeout(() => {
            transitionToSynapse(response.token_count);
        }, 800);

    } catch (error) {
        elements.termText.innerText = `Error: ${error.message}`;
        elements.termText.style.color = "#ef4444";
        setTimeout(() => {
            elements.processingOverlay.classList.add('hidden');
            store.isProcessing = false;
        }, 2000);
    }
}

function transitionToSynapse(tokens) {
    // 1. Animate Out Ingestion
    gsap.to("#view-ingestion", {
        opacity: 0,
        duration: 0.5,
        onComplete: () => {
            elements.viewIngestion.classList.add('hidden');
            elements.viewSynapse.classList.remove('hidden');
            
            // Update Data
            elements.metaFilename.innerText = store.currentFile;
            elements.metaSize.innerText = store.fileSize;
            elements.metaTokens.innerText = tokens || "Unknown";
            elements.chatIntroFilename.innerText = store.currentFile;
            
            // 2. Animate In Synapse
            gsap.from(".sidebar", {x: -50, opacity: 0, duration: 0.6, delay: 0.1});
            gsap.from(".chat-header", {y: -20, opacity: 0, duration: 0.6, delay: 0.2});
            gsap.from(".chat-stream", {opacity: 0, duration: 0.6, delay: 0.4});
            gsap.from(".input-dock", {y: 20, opacity: 0, duration: 0.6, delay: 0.5});
            
            elements.chatInput.focus();
        }
    });
}

// 2. CHAT
async function sendMessage() {
    const query = elements.chatInput.value.trim();
    if (!query || !store.sessionId) return;

    // Add User Message
    addMessageToStream('user', query);
    elements.chatInput.value = '';
    elements.chatInput.style.height = 'auto';

    // Show Typing Indicator (Fake)
    const typingId = showTypingIndicator();

    try {
        const data = await sendRequest('/chat', {
            session_id: store.sessionId,
            query: query
        }, 'json');

        removeTypingIndicator(typingId);
        addMessageToStream('ai', data.response);

    } catch (error) {
        removeTypingIndicator(typingId);
        addMessageToStream('ai', `**System Error:** ${error.message}`);
    }
}

function addMessageToStream(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    
    let contentHtml = '';
    
    if (role === 'ai') {
        // Parse Markdown with Marked.js
        contentHtml = marked.parse(text);
    } else {
        contentHtml = `<p>${text.replace(/\n/g, '<br>')}</p>`;
    }

    div.innerHTML = `
        <div class="avatar">
            <i class="ph-fill ${role === 'ai' ? 'ph-sparkle' : 'ph-user'}"></i>
        </div>
        <div class="content glass-bubble">
            ${contentHtml}
        </div>
    `;
    
    elements.chatStream.appendChild(div);
    
    // Highlight Code Blocks
    div.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    // Scroll to bottom
    requestAnimationFrame(() => {
        elements.chatStream.scrollTo({
            top: elements.chatStream.scrollHeight,
            behavior: 'smooth'
        });
    });
}

// UI HELPERS
function showTypingIndicator() {
    const id = "typing-" + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = "message ai";
    div.innerHTML = `
        <div class="avatar"><i class="ph-fill ph-sparkle"></i></div>
        <div class="content glass-bubble">
            <div class="model-status"><span class="pulse">Thinking...</span></div>
        </div>
    `;
    elements.chatStream.appendChild(div);
    elements.chatStream.scrollTop = elements.chatStream.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// --- EVENTS ---
elements.dropZone.addEventListener('click', () => elements.fileInput.click());
elements.dropZone.addEventListener('dragover', (e) => { e.preventDefault(); elements.dropZone.classList.add('drag-active'); });
elements.dropZone.addEventListener('dragleave', (e) => { e.preventDefault(); elements.dropZone.classList.remove('drag-active'); });
elements.dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.dropZone.classList.remove('drag-active');
    if (e.dataTransfer.files[0]) handleIngestion('file', e.dataTransfer.files[0]);
});
elements.fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleIngestion('file', e.target.files[0]);
});

elements.scrapeBtn.addEventListener('click', () => {
    if (elements.urlInput.value) handleIngestion('url', elements.urlInput.value);
});

elements.sendBtn.addEventListener('click', sendMessage);
elements.chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
elements.chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

elements.resetBtn.addEventListener('click', async () => {
    if (confirm("Purge neural memory and reset?")) {
        try {
            console.log("Sending purge request...");
            // Added specific headers and method to ensure connectivity
            const res = await fetch(`${API_BASE}/reset`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            
            if (res.ok) {
                console.log("Purge successful");
            } else {
                console.error("Purge failed on backend");
            }
        } catch(e) {
            console.error("Network error during purge:", e);
        } finally {
            // Only reload after the attempt is finished
            setTimeout(() => location.reload(), 200);
        }
    }
});