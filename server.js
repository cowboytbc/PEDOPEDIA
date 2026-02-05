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
                messages: messages,
                temperature: 0.3,
                max_tokens: 1000
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
