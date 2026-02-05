// AI Chat functionality
// IMPORTANT: The API key should be stored server-side, not in this file
// For now, user needs to set it up properly

let chatHistory = [];
let apiKey = null;

// Load API key from environment or prompt user
async function initializeChat() {
    // Try to load from server endpoint (if you set one up)
    try {
        const response = await fetch('/api/config');
        if (response.ok) {
            const config = await response.json();
            apiKey = config.apiKey;
        }
    } catch (e) {
        // If no server endpoint, user must enter API key
        console.log('No API endpoint found. User must configure API key.');
    }
}

function toggleChat() {
    const widget = document.getElementById('chatWidget');
    widget.classList.toggle('collapsed');
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Check if API key is set
    if (!apiKey) {
        showChatMessage('error', '⚠️ API KEY NOT CONFIGURED. Please set up your OpenAI API key in the .env file and create a server endpoint, OR use the simple version without AI chat.');
        return;
    }
    
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
        
        // Call OpenAI API
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-4',
                messages: [
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
                ],
                temperature: 0.3,
                max_tokens: 1000
            })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
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
        
        showChatMessage('error', `❌ Error: ${error.message}. Please check your API key configuration.`);
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
