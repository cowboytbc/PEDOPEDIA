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
    results.forEach(result => {
        const excerpt = getExcerpt(result.content, query, result.matches[0]);
        html += `
            <div class="result-item">
                <div class="result-header">
                    <div class="result-title">${escapeHtml(result.title)}</div>
                    <div class="result-meta">${result.relevance} match${result.relevance !== 1 ? 'es' : ''}</div>
                </div>
                <div class="result-excerpt">${excerpt}</div>
                <div class="result-footer">
                    <span>Source: ${escapeHtml(result.source)}</span>
                    ${result.date ? `<span>Date: ${escapeHtml(result.date)}</span>` : ''}
                    ${result.page ? `<span>Page: ${escapeHtml(result.page)}</span>` : ''}
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
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
