# ⚖️ Epstein Files Search - Official Court Documents Database

**FACTS ONLY. NO SPECULATION. OFFICIAL RECORDS.**

A searchable database of official Epstein court documents with AI-powered assistance for understanding the files.

## 🎯 Purpose

This tool provides searchable access to official, publicly available court documents related to Jeffrey Epstein cases. All documents are from verified sources including U.S. Federal Courts, CourtListener, and PACER.

## ⚠️ IMPORTANT - About "Pizzagate"

**There is no "Pizzagate" section** because Pizzagate was a debunked conspiracy theory with NO official court documents. This project only includes **verified, official court records** from actual legal proceedings.

## 🔒 Features

- **Full-Text Search**: Search across all documents by name, term, or phrase
- **AI Chat Assistant**: Ask questions about the documents (requires OpenAI API)
- **Document Library**: Browse all included files by source
- **Source Attribution**: Every result shows exact source, case number, and page
- **Automated Updates**: Downloads newly unsealed documents

## 📁 Included Sources

### Primary Sources:
- **Giuffre v. Maxwell** (Case 1:15-cv-07433-LAP) - S.D. New York
- **United States v. Epstein** (Case 1:08-cr-10435) - S.D. Florida  
- **United States v. Maxwell** (Case 1:20-cr-00330) - S.D. New York
- FBI Records Vault releases
- Other unsealed federal court documents

## 🚀 Quick Start

### Prerequisites
```bash
pip install selenium webdriver-manager pdfplumber requests
```

### 1. Download Documents
```bash
python selenium_downloader.py
```

### 2. Extract Text
```bash
python process_all_pdfs.py
```

### 3. Open Website
Just open `index.html` in your browser!

## 🔐 CRITICAL: API Key Security

### ⚠️ NEVER COMMIT API KEYS TO GITHUB

1. Create `.env` file (already in .gitignore):
   ```
   OPENAI_API_KEY=your_key_here
   ```

2. For production, use a backend server - **DO NOT** put API keys in JavaScript

3. The AI chat feature requires proper server setup for security

## ⚖️ Legal & Ethical Use

### This Project Provides:
✅ Official court records  
✅ Verified sources only  
✅ Proper attribution  

### NOT Included:
❌ Speculation  
❌ Conspiracy theories  
❌ Sealed documents  
❌ Private information

Use responsibly. Court allegations ≠ proven facts.

## 📜 License

MIT License

## ⚠️ Disclaimer

For educational/research purposes. Not legal advice. Verify all information with original sources.

---

**Official Sources**: [CourtListener](https://www.courtlistener.com/) • [PACER](https://pacer.uscourts.gov/) • [FBI Vault](https://vault.fbi.gov/)
