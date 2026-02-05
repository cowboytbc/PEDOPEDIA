// Serverless function for Vercel/Netlify
// This protects your API key by running server-side

export default async function handler(req, res) {
    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // Get API key from environment variable (GitHub Secret)
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey) {
        return res.status(500).json({ error: 'API key not configured' });
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
            throw new Error(`OpenAI API error: ${response.status}`);
        }

        const data = await response.json();
        return res.status(200).json(data);

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ error: error.message });
    }
}
