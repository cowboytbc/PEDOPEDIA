const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 10000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// API endpoint for chat (protects API key)
app.post('/api/chat', async (req, res) => {
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey) {
        return res.status(500).json({ 
            error: 'API key not configured. Set OPENAI_API_KEY in Render environment variables.' 
        });
    }

    try {
        const { messages } = req.body;

        // Call OpenAI API server-side
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
                        content: `You are a STRICTLY FACTUAL assistant for PEDOPEDIA, an official court documents database. CRITICAL RULES:
1. ONLY answer questions using information EXPLICITLY found in the provided court documents
2. NEVER speculate, infer, or use outside knowledge
3. ALWAYS cite the specific document name and page when making ANY claim
4. If information is NOT in the documents, say "This information is not found in the available court documents"
5. Maintain complete neutrality and objectivity - present only what the documents state
6. Quote exact text from documents when possible
7. Never express opinions or make judgments beyond what documents explicitly state
8. If asked about something not in documents, respond: "I can only answer based on the official court documents in this database. That information is not available in the current document set."

Your purpose is to help users find FACTUAL INFORMATION from OFFICIAL COURT RECORDS - nothing more.`
                    },
                    ...messages
                ],
                temperature: 0.1,
                max_tokens: 1500
            })
        });

        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(`OpenAI API error: ${response.status} - ${errorData}`);
        }

        const data = await response.json();
        res.json(data);

    } catch (error) {
        console.error('API Error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Serve index.html for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 PEDOPEDIA server running on port ${PORT}`);
    console.log(`🔐 API key configured: ${process.env.OPENAI_API_KEY ? 'YES' : 'NO'}`);
});
