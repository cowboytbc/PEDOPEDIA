// AI Chat functionality
// API key is now stored as GitHub Secret and used server-side

let chatHistory = [];

// No need to initialize API key - it's server-side now
async function initializeChat() {
    console.log('Chat initialized - using secure server-side API');
}

function toggleChat() {
    const widget = document.getElementById('chatWidget');
    widget.classList.toggle('collapsed');
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    showChatMessage('user', message);
    input.value = '';
    
    // Add to history
    chatHistory.push({
        role: 'user',
        content: message
    });
    
    // Show thinking indicator
    const thinkingId = showChatMessage('ai', '🤔 Analyzing documents...');
    
    try {
        // Prepare context from documents
        const context = prepareDocumentContext(message);
        
        // Prepare messages for API
        const messages = [
            {
                role: 'system',
                content: `You are an AI assistant helping users understand official Epstein court documents. 
                
CRITICAL RULES:
1. ONLY provide information based on the actual documents in the database
2. NEVER speculate or make assumptions
3. ALWAYS cite the specific document source (case number, entry number, page)
4. If information is not in the documents, say so clearly
5. Be factual, objective, and careful with sensitive information
6. Remind users that these are official court records, not verified facts

Context from documents:
${context}`
            },
            ...chatHistory
        ];
        
        // Call our secure server-side API endpoint on Render
        const RENDER_API_URL = 'https://pedopedia.onrender.com/api/chat';
        
        const response = await fetch(RENDER_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ messages })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `API Error: ${response.status}`);
        }
        
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        // Remove thinking indicator
        const thinkingEl = document.getElementById(thinkingId);
        if (thinkingEl) thinkingEl.remove();
        
        // Add AI response
        showChatMessage('ai', aiResponse);
        
        // Add to history
        chatHistory.push({
            role: 'assistant',
            content: aiResponse
        });
        
    } catch (error) {
        console.error('Chat error:', error);
        
        // Remove thinking indicator
        const thinkingEl = document.getElementById(thinkingId);
        if (thinkingEl) thinkingEl.remove();
        
        showChatMessage('error', `❌ Error: ${error.message}\n\nMake sure you've deployed to Vercel/Netlify and set the OPENAI_API_KEY secret.`);
    }
}

function prepareDocumentContext(query) {
    // Search documents for relevant context
    if (!documentDatabase || documentDatabase.length === 0) {
        return 'No documents loaded yet.';
    }
    
    // Do a quick search for relevant docs
    const relevantDocs = searchDocuments(query, true, false).slice(0, 5);
    
    if (relevantDocs.length === 0) {
        return 'No relevant documents found for this query.';
    }
    
    // Prepare context
    let context = `Relevant documents found:\n\n`;
    relevantDocs.forEach(doc => {
        const excerpt = doc.content.substring(0, 500);
        context += `[${doc.source}] ${doc.title}\n${excerpt}...\n\n`;
    });
    
    return context;
}

function showChatMessage(type, content) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageEl = document.createElement('div');
    const messageId = 'msg-' + Date.now();
    messageEl.id = messageId;
    messageEl.className = `chat-message ${type}`;
    messageEl.textContent = content;
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageId;
}

// Handle Enter key in chat input
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    initializeChat();
});

function toggleLibrary() {
    const panel = document.getElementById('libraryPanel');
    panel.classList.toggle('collapsed');
}

function populateDocumentLibrary() {
    const listEl = document.getElementById('documentList');
    const countEl = document.getElementById('docCount');
    
    if (!documentDatabase || documentDatabase.length === 0) {
        listEl.innerHTML = '<p style="color: #6b7280;">No documents loaded yet.</p>';
        return;
    }
    
    countEl.textContent = documentDatabase.length;
    
    // Group by source
    const bySource = {};
    documentDatabase.forEach(doc => {
        const source = doc.source || 'Unknown';
        if (!bySource[source]) {
            bySource[source] = [];
        }
        bySource[source].push(doc);
    });
    
    let html = '';
    for (const [source, docs] of Object.entries(bySource)) {
        html += `<div class="doc-list-item">
            <strong>${escapeHtml(source)}</strong> (${docs.length} document${docs.length > 1 ? 's' : ''})
        </div>`;
    }
    
    listEl.innerHTML = html;
}
