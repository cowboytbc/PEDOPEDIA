# 🚀 DEPLOY TO RENDER - STEP BY STEP

## Step 1: Create Render Account

1. Go to **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your GitHub

---

## Step 2: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your repository:
   - Click **"Connect account"** if needed
   - Find and select **cowboytbc/PEDOPEDIA**
   - Click **"Connect"**

---

## Step 3: Configure Your Service

### Basic Settings:
- **Name**: `pedopedia` (or whatever you want)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Node`
- **Build Command**: `npm install`
- **Start Command**: `npm start`

### Instance Type:
- Select **"Free"** (perfect for testing)

---

## Step 4: Add Environment Variable (SECRET API KEY)

**THIS IS THE IMPORTANT PART!**

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Fill in:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (get from https://platform.openai.com/api-keys)
4. Click **"Add"**

⚠️ **Make sure you use a NEW API key** (revoke the one you posted earlier!)

---

## Step 5: Deploy!

1. Click **"Create Web Service"** at the bottom
2. Render will:
   - Clone your repo
   - Install dependencies
   - Start the server
   - Deploy your site

⏱️ This takes 2-5 minutes

---

## Step 6: Get Your Live URL

Once deployed, you'll get a URL like:
**https://pedopedia.onrender.com**

Your site is now LIVE and secure! 🎉

---

## Step 7: Test the AI Chat

1. Open your live URL
2. Click the AI chat widget (bottom right)
3. Ask a question
4. The AI should respond using your documents

✅ Your API key is secure and never exposed!

---

## Managing Your Site

### View Logs:
- Click on your service
- Go to **"Logs"** tab
- See real-time server activity

### Update Environment Variables:
- Service → **"Environment"** tab
- Edit/add variables
- Click **"Save Changes"**

### Redeploy:
- Every git push to `main` automatically redeploys!
- Or click **"Manual Deploy"** → **"Deploy latest commit"**

---

## Free Tier Limits

Render Free tier includes:
- ✅ 750 hours/month (enough for 24/7)
- ✅ Auto-deploys from GitHub
- ✅ HTTPS included
- ⚠️ Spins down after 15 min of inactivity (wakes up in ~30 seconds)

---

## Troubleshooting

### If deploy fails:
1. Check **"Logs"** tab for errors
2. Make sure `package.json` and `server.js` are in repo
3. Verify `OPENAI_API_KEY` is set in Environment Variables

### If AI chat doesn't work:
1. Check browser console for errors (F12)
2. Verify Environment Variable is set
3. Check Render logs for API errors

---

## Custom Domain (Optional)

Want your own domain like `pedopedia.com`?

1. Buy domain (Namecheap, Google Domains, etc.)
2. In Render: **"Settings"** → **"Custom Domain"**
3. Add your domain
4. Update DNS records as shown
5. Done! (Takes a few hours to propagate)

---

## That's It!

Your PEDOPEDIA is now:
- ✅ Live on the internet
- ✅ Fully secure (API key hidden)
- ✅ Auto-updates from GitHub
- ✅ Professional and fast

**Ready to deploy?** Push the latest code and follow these steps!
