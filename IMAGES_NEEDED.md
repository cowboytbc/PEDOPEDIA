# 🖼️ MISSING IMAGES

You need to add these image files to your repository:

## Required Images:

### 1. **banner.png**
- Location: Root directory (next to index.html)
- Recommended size: 1200px x 250px
- Format: PNG
- Purpose: Top banner across the site

### 2. **logo.png**  
- Location: Root directory (next to index.html)
- Recommended size: 200px x 200px (or square ratio)
- Format: PNG  
- Purpose: Site logo next to "PEDOPEDIA" title

---

## How to Add Images:

### Option 1: Upload via GitHub Web Interface
1. Go to https://github.com/cowboytbc/PEDOPEDIA
2. Click **"Add file"** → **"Upload files"**
3. Drag `banner.png` and `logo.png` into the browser
4. Write commit message: "Add banner and logo images"
5. Click **"Commit changes"**
6. Render will auto-redeploy with the images!

### Option 2: Upload via Git Command Line
```powershell
# Put banner.png and logo.png in this folder, then:
git add banner.png logo.png
git commit -m "Add banner and logo images"
git push
```

---

## Current Status:
✅ Site works without images (onerror handler hides them)
⚠️ Images will show 404 errors in console until uploaded
✅ Once uploaded, they'll appear automatically

---

## Design Tips:
- **Banner**: Wide, aggressive red/black aesthetic
- **Logo**: Square or circular, bold design
- Use high contrast colors to match the site theme
- Compress images before uploading (tinypng.com)

Once you add these files to GitHub, they'll appear on your live Render site automatically!
