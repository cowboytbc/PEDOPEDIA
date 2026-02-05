// Document database - This will hold the indexed documents
let documentDatabase = [];
let searchIndex = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadDocuments();
    setupEventListeners();
});

function setupEventListeners() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

// Load documents from the data file
async function loadDocuments() {
    try {
        const response = await fetch('documents.json');
        if (!response.ok) {
            console.warn('No documents.json file found. Please add documents to enable search.');
            return;
        }
        const data = await response.json();
        documentDatabase = data.documents || [];
        buildSearchIndex();
        updateLastUpdated(data.lastUpdated);
        updateTotalDocs(documentDatabase.length);
        populateDocumentLibrary();
    } catch (error) {
        console.warn('Could not load documents:', error.message);
    }
}

function updateTotalDocs(count) {
    const totalDocsEl = document.getElementById('totalDocs');
    if (totalDocsEl) {
        totalDocsEl.textContent = count;
    }
}

// Build a search index for faster lookups
function buildSearchIndex() {
    searchIndex = {};
    documentDatabase.forEach((doc, index) => {
        const text = `${doc.title} ${doc.content} ${doc.source}`.toLowerCase();
        const words = text.split(/\s+/);
        
        words.forEach(word => {
            if (!searchIndex[word]) {
                searchIndex[word] = [];
            }
            if (!searchIndex[word].includes(index)) {
                searchIndex[word].push(index);
            }
        });
    });
}

// Perform search
function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    const caseInsensitive = document.getElementById('caseInsensitive').checked;
    const exactMatch = document.getElementById('exactMatch').checked;
    
    if (!query) {
        showMessage('Please enter a search term.');
        return;
    }
    
    if (documentDatabase.length === 0) {
        showMessage('No documents loaded. Please add documents.json file with official Epstein files.');
        return;
    }
    
    showLoading();
    
    // Simulate slight delay for better UX
    setTimeout(() => {
        const results = searchDocuments(query, caseInsensitive, exactMatch);
        displayResults(results, query);
    }, 300);
}

// Search through documents
function searchDocuments(query, caseInsensitive, exactMatch) {
    const searchQuery = caseInsensitive ? query.toLowerCase() : query;
    const results = [];
    
    documentDatabase.forEach((doc, index) => {
        const content = caseInsensitive ? doc.content.toLowerCase() : doc.content;
        const title = caseInsensitive ? doc.title.toLowerCase() : doc.title;
        
        let matches = [];
        
        if (exactMatch) {
            // Exact phrase match
            const regex = new RegExp(escapeRegex(searchQuery), caseInsensitive ? 'gi' : 'g');
            let match;
            while ((match = regex.exec(doc.content)) !== null) {
                matches.push(match.index);
            }
        } else {
            // Flexible search - find documents containing the terms
            const searchTerms = searchQuery.split(/\s+/);
            let found = searchTerms.every(term => 
                content.includes(term) || title.includes(term)
            );
            
            if (found) {
                // Find all occurrences for highlighting
                searchTerms.forEach(term => {
                    const regex = new RegExp(escapeRegex(term), caseInsensitive ? 'gi' : 'g');
                    let match;
                    while ((match = regex.exec(doc.content)) !== null) {
                        matches.push(match.index);
                    }
                });
            }
        }
        
        if (matches.length > 0) {
            results.push({
                ...doc,
                matches: matches,
                relevance: matches.length
            });
        }
    });
    
    // Sort by relevance (number of matches)
    results.sort((a, b) => b.relevance - a.relevance);
    
    return results;
}

// Display search results
function displayResults(results, query) {
    const resultsDiv = document.getElementById('results');
    const statsDiv = document.getElementById('stats');
    
    if (results.length === 0) {
        statsDiv.innerHTML = `No results found for "${escapeHtml(query)}"`;
        resultsDiv.innerHTML = `
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try different search terms or check your spelling.</p>
            </div>
        `;
        return;
    }
    
    statsDiv.innerHTML = `Found ${results.length} document${results.length !== 1 ? 's' : ''} matching "${escapeHtml(query)}"`;
    
    let html = '';
    results.forEach((result, index) => {
        const excerpt = getExcerpt(result.content, query, result.matches[0]);
        const resultId = `result-${index}`;
        const fullContentId = `full-content-${index}`;
        const aiExplainId = `ai-explain-${index}`;
        
        html += `
            <div class="result-item">
                <div class="result-header" onclick="toggleResultExpand('${resultId}')">
                    <div class="result-title-group">
                        <span class="expand-icon" id="icon-${resultId}">▶</span>
                        <div class="result-title">${escapeHtml(result.title)}</div>
                    </div>
                    <div class="result-meta">${result.relevance} match${result.relevance !== 1 ? 'es' : ''}</div>
                </div>
                
                <div class="result-excerpt">${excerpt}</div>
                
                <div class="result-full-content collapsed" id="${fullContentId}">
                    <div class="full-text">${escapeHtml(result.content).replace(/\n/g, '<br>')}</div>
                </div>
                
                <div class="result-actions">
                    <button class="action-btn expand-btn" onclick="toggleFullContent('${fullContentId}', '${resultId}')">
                        <span id="expand-text-${resultId}">Read Full Document</span>
                    </button>
                    <button class="action-btn ai-btn" onclick="explainWithAI('${aiExplainId}', ${index})">
                        🤖 AI Explain in Simple Terms
                    </button>
                </div>
                
                <div class="ai-explanation collapsed" id="${aiExplainId}">
                    <div class="ai-loading">Analyzing document with AI...</div>
                </div>
                
                <div class="result-footer">
                    <span>Source: ${escapeHtml(result.source)}</span>
                    ${result.date ? `<span>Date: ${escapeHtml(result.date)}</span>` : ''}
                    ${result.page ? `<span>Page: ${escapeHtml(result.page)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
    
    // Store results globally for AI explanations
    window.currentSearchResults = results;
}

// Get an excerpt from the content with highlighted search terms
function getExcerpt(content, query, matchPosition = 0) {
    const excerptLength = 300;
    const start = Math.max(0, matchPosition - 100);
    const end = Math.min(content.length, start + excerptLength);
    
    let excerpt = content.substring(start, end);
    
    // Add ellipsis if truncated
    if (start > 0) excerpt = '...' + excerpt;
    if (end < content.length) excerpt = excerpt + '...';
    
    // Highlight search terms
    const terms = query.toLowerCase().split(/\s+/);
    terms.forEach(term => {
        const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
        excerpt = excerpt.replace(regex, '<mark>$1</mark>');
    });
    
    return excerpt;
}

// Helper functions
function showLoading() {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<div class="loading">Searching</div>';
    document.getElementById('stats').innerHTML = '';
}

function showMessage(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="no-results">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function updateLastUpdated(date) {
    const lastUpdateSpan = document.getElementById('lastUpdate');
    if (date) {
        lastUpdateSpan.textContent = date;
    } else {
        lastUpdateSpan.textContent = 'No data loaded';
    }
}

// Populate document library
function populateDocumentLibrary() {
    const docList = document.getElementById('documentList');
    const docCount = document.getElementById('docCount');
    
    if (!docList) return;
    
    docCount.textContent = documentDatabase.length;
    
    if (documentDatabase.length === 0) {
        docList.innerHTML = '<p style="color: #fca5a5; padding: 20px;">No documents loaded yet.</p>';
        return;
    }
    
    docList.innerHTML = documentDatabase.map((doc, index) => {
        // Extract case number from filename for CourtListener URL
        const filename = doc.filename || '';
        const courtListenerUrl = `https://www.courtlistener.com/docket/4355308/giuffre-v-maxwell/`;
        
        return `
            <div class="doc-list-item">
                <strong>${index + 1}.</strong> ${escapeHtml(doc.title || 'Untitled Document')}
                <br>
                <span style="font-size: 0.85em; color: #fca5a5;">
                    ${escapeHtml(doc.source || 'Unknown source')} 
                    ${doc.date ? ` • ${escapeHtml(doc.date)}` : ''}
                </span>
                <br>
                <a href="${courtListenerUrl}" target="_blank" rel="noopener noreferrer" 
                   style="color: #dc2626; font-weight: 700; text-decoration: none; font-size: 0.9em;">
                    📄 View on CourtListener →
                </a>
            </div>
        `;
    }).join('');
}

// Toggle document library visibility
function toggleLibrary() {
    const panel = document.getElementById('libraryPanel');
    panel.classList.toggle('collapsed');
}

// Toggle hamburger menu
function toggleMenu() {
    const overlay = document.getElementById('menuOverlay');
    overlay.classList.toggle('active');
    document.body.style.overflow = overlay.classList.contains('active') ? 'hidden' : '';
}

// Scroll to footer (token info)
function scrollToFooter() {
    document.querySelector('footer').scrollIntoView({ behavior: 'smooth' });
    toggleMenu();
}

// Copy CA address
function copyCA() {
    const caAddress = document.getElementById('caAddress').textContent;
    navigator.clipboard.writeText(caAddress).then(() => {
        const btn = event.target.closest('.copy-btn');
        btn.classList.add('copied');
        setTimeout(() => btn.classList.remove('copied'), 2000);
    });
}

// Toggle result expansion
function toggleResultExpand(resultId) {
    const icon = document.getElementById(`icon-${resultId}`);
    if (icon.textContent === '▶') {
        icon.textContent = '▼';
    } else {
        icon.textContent = '▶';
    }
}

// Toggle full content visibility
function toggleFullContent(contentId, resultId) {
    const content = document.getElementById(contentId);
    const textEl = document.getElementById(`expand-text-${resultId}`);
    const isCollapsed = content.classList.contains('collapsed');
    
    content.classList.toggle('collapsed');
    textEl.textContent = isCollapsed ? 'Hide Full Document' : 'Read Full Document';
}

// Explain search result with AI
async function explainWithAI(explainId, resultIndex) {
    const explainDiv = document.getElementById(explainId);
    const result = window.currentSearchResults[resultIndex];
    
    // Toggle if already open
    if (!explainDiv.classList.contains('collapsed') && explainDiv.querySelector('.ai-response')) {
        explainDiv.classList.add('collapsed');
        return;
    }
    
    explainDiv.classList.remove('collapsed');
    explainDiv.innerHTML = '<div class="ai-loading">🤖 Analyzing document with AI...</div>';
    
    try {
        const response = await fetch('https://pedopedia.onrender.com/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: `Explain this court document in simple, layman's terms. What does it mean? What's important? Be concise and clear:\n\nDocument: ${result.title}\nContent: ${result.content.substring(0, 2000)}`
            })
        });
        
        if (!response.ok) throw new Error('AI service unavailable');
        
        const data = await response.json();
        explainDiv.innerHTML = `
            <div class="ai-response">
                <div class="ai-header">🤖 AI Explanation (Simple Terms)</div>
                <div class="ai-text">${escapeHtml(data.response).replace(/\n/g, '<br>')}</div>
            </div>
        `;
    } catch (error) {
        explainDiv.innerHTML = `
            <div class="ai-error">
                ⚠️ AI explanation unavailable. The AI service may be down or you may need to add an API key to the backend.
            </div>
        `;
    }
}
