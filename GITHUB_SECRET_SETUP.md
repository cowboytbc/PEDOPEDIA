# 🔐 SETTING UP GITHUB SECRET FOR API KEY

## Step 1: Add Secret to GitHub

1. Go to: **https://github.com/cowboytbc/PEDOPEDIA/settings/secrets/actions**

2. Click **"New repository secret"**

3. Name: `OPENAI_API_KEY`

4. Value: Your OpenAI API key (get a NEW one from https://platform.openai.com/api-keys)

5. Click **"Add secret"**

## Step 2: Deploy to Vercel (Easiest Option)

### Option A: Deploy with Vercel

1. Go to: **https://vercel.com**

2. Sign in with GitHub

3. Click **"Import Project"**

4. Select **cowboytbc/PEDOPEDIA**

5. In settings, add Environment Variable:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

6. Click **Deploy**

Your site will be live at: `https://pedopedia.vercel.app` (or similar)

### Option B: Deploy with Netlify

1. Go to: **https://netlify.com**

2. Sign in with GitHub

3. Click **"Add new site"** → **"Import an existing project"**

4. Select **cowboytbc/PEDOPEDIA**

5. In **"Site settings"** → **"Environment variables"**, add:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

6. Deploy!

## Step 3: Enable GitHub Pages (Optional - for free hosting)

1. Go to: **https://github.com/cowboytbc/PEDOPEDIA/settings/pages**

2. Source: **main branch**

3. Click **Save**

Your site will be at: `https://cowboytbc.github.io/PEDOPEDIA/`

**Note**: GitHub Pages doesn't support serverless functions, so you'll need Vercel or Netlify for the AI chat to work.

## Why This Is Secure

✅ API key is stored as a secret (encrypted)  
✅ Never exposed in browser/JavaScript  
✅ Only accessible server-side  
✅ Not in GitHub code history  
✅ Can be rotated without code changes

## Testing

After deploying:

1. Open your deployed site
2. Click the AI chat widget
3. Ask a question
4. It will use the server-side API with your secret key

The API key is NEVER visible in the browser!
