# COMPLETE SETUP GUIDE
# How to Download and Process ALL Epstein Documents

## Quick Start (3 Steps)

### Step 1: Install Requirements
```powershell
pip install requests pdfplumber tqdm
```

### Step 2: Download ALL Documents
```powershell
python download_all_documents.py
```

This will:
- ✅ Connect to CourtListener API (official court records)
- ✅ Download ALL available documents from major Epstein cases:
  - Giuffre v. Maxwell (1:15-cv-07433) - Hundreds of documents
  - United States v. Epstein (1:08-cr-10435)
  - United States v. Maxwell (1:20-cr-00330)
- ✅ Save PDFs to `epstein_documents/pdfs/`
- ✅ Track progress in `download_log.json` (resume if interrupted)
- ✅ Can be run multiple times - skips already downloaded files

### Step 3: Extract Text from All PDFs
```powershell
python process_all_pdfs.py
```

This will:
- ✅ Read all downloaded PDFs
- ✅ Extract text from every page
- ✅ Create complete `documents.json` database
- ✅ Generate statistics report

### Step 4: Use Your Search Tool
```powershell
# Just open in browser
start index.html
```

Search through ALL official documents instantly!

---

## What Gets Downloaded

### Major Cases Covered:

**1. Giuffre v. Maxwell (Civil Case)**
- Case Number: 1:15-cv-07433-LAP
- Court: Southern District of New York
- Contents: Depositions, emails, flight logs, witness statements
- Status: Hundreds of documents unsealed

**2. United States v. Epstein (Criminal)**
- Case Number: 1:08-cr-10435
- Court: Southern District of Florida
- Contents: Criminal case filings, plea agreements

**3. United States v. Maxwell (Criminal)**
- Case Number: 1:20-cr-00330
- Court: Southern District of New York
- Contents: Criminal trial documents, evidence exhibits

---

## Features of the Downloader

### Automatic & Comprehensive
- Downloads EVERY publicly available document
- Automatically searches for related cases
- Resumes if interrupted (maintains download log)
- Skips already downloaded files
- Organized by case and entry number

### Safe & Legal
- Only public court records
- Official CourtListener API
- Respects server rate limits
- Includes proper attribution
- No authentication required

### Progress Tracking
- Real-time progress display
- Downloadlog.json tracks everything
- Can pause and resume anytime
- Summary report when complete

---

## File Structure After Download

```
epstein_documents/
├── pdfs/
│   ├── Giuffre_v_Maxwell_1_Complaint.pdf
│   ├── Giuffre_v_Maxwell_5_Motion.pdf
│   ├── Giuffre_v_Maxwell_50_Deposition.pdf
│   └── ... (hundreds more)
├── json/
├── download_log.json
├── DOWNLOAD_SUMMARY.txt
└── STATISTICS.txt

documents.json (created by process_all_pdfs.py)
index.html (your search interface)
```

---

## Expected Results

### Document Counts (Approximate):
- **Giuffre v. Maxwell**: 200-500+ documents
- **Other cases**: 50-200+ documents
- **Total**: 300-700+ official documents

### Time Estimates:
- **Download**: 30-120 minutes (depends on connection)
- **Text extraction**: 15-60 minutes (depends on PDF sizes)
- **Total**: 1-3 hours for COMPLETE database

---

## Troubleshooting

### If Download Stops:
```powershell
# Just run again - it will resume
python download_all_documents.py
```

### If You Get Rate Limited:
The script includes delays, but if needed:
- Wait 10-15 minutes
- Run again (progress is saved)
- Script will continue where it left off

### If a PDF Won't Extract:
- Noted in `failed_extractions.txt`
- Usually OCR scans that need special processing
- Main database still includes all others

---

## Alternative: Manual Download

If you prefer manual control:

### Option 1: CourtListener Website
1. Visit: https://www.courtlistener.com/docket/4355308/giuffre-v-maxwell/
2. Click each document entry
3. Click "Download PDF"
4. Save to `epstein_documents/pdfs/`

### Option 2: PACER Direct
1. Register at: https://pacer.uscourts.gov/
2. Search case numbers
3. Download documents ($0.10/page, often free)

Then run: `python process_all_pdfs.py` to extract text

---

## Verification

Every document includes:
- ✅ Case number and name
- ✅ Entry/docket number
- ✅ Court seal and stamps
- ✅ Official court formatting
- ✅ Source attribution

All from official court records - no secondary sources!

---

## Legal Notes

- All documents are PUBLIC RECORDS
- Released by federal courts
- Not subject to seal or protective orders
- Properly attributed with case numbers
- Educational/research purposes

---

## Next Steps After Setup

1. **Open search tool**: `start index.html`
2. **Search anything**: Names, places, dates, events
3. **Verify sources**: Every result shows case number and entry
4. **Share responsibly**: Facts from official documents only

---

## Questions?

Check these files:
- `DOWNLOAD_SUMMARY.txt` - What was downloaded
- `STATISTICS.txt` - Document counts and info
- `download_log.json` - Complete download history
- `failed_extractions.txt` - Any problem files

---

## Updates

To get newly released documents:
```powershell
# Just run the downloader again
python download_all_documents.py

# Then re-extract
python process_all_pdfs.py
```

It will only download NEW documents!

---

**Ready to start?**

```powershell
pip install requests pdfplumber tqdm
python download_all_documents.py
```
