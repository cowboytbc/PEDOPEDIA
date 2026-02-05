# ADDITIONAL EPSTEIN DOCUMENT SOURCES

## 🎯 PRIORITY SOURCES TO ADD

### 1. FBI VAULT - Jeffrey Epstein Files
**URL:** https://vault.fbi.gov/jeffrey-epstein
- **Content:** FBI investigation files, interviews, evidence
- **Status:** Partially released under FOIA
- **Contains:** Victim statements, flight logs, financial records, surveillance reports
- **Implementation:** Need web scraper for FBI Vault PDF downloads

### 2. Department of Justice (DOJ) Releases
**Sources:**
- **Southern District of New York (SDNY):** https://www.justice.gov/usao-sdny
- **Southern District of Florida (SDFL):** https://www.justice.gov/usao-sdfl
- **Press Releases:** Search "Epstein" in DOJ press releases for linked documents
- **Non-Prosecution Agreement (2008):** Miami Herald FOIA releases
- **Contains:** Indictments, plea agreements, victim impact statements, investigation reports

### 3. Flight Logs & Travel Records
**Known Sources:**
- **Gawker Release (2015):** Flight manifest PDFs (already archived online)
- **Court Exhibits:** Embedded in Giuffre v. Maxwell and other cases
- **Black Book:** Contact lists submitted as court evidence
- **Implementation:** 
  - Download from Internet Archive: https://archive.org/details/EpsteinFlightLogsLolitaExpress
  - Extract from existing court exhibits in CourtListener docs

### 4. Ghislaine Maxwell Trial Documents
**Source:** SDNY Case 1:20-cr-00330-AJN
- **Location:** CourtListener + PACER
- **Contains:** Trial exhibits, victim testimony transcripts, evidence photos, emails
- **Status:** Many documents unsealed in 2021-2023
- **Implementation:** Already partially covered by our CourtListener scraper, need to verify completeness

### 5. Virginia Giuffre Deposition & Photos
**Sources:**
- **Giuffre v. Maxwell (SDNY):** Full deposition transcripts
- **Photo Evidence:** Images submitted as exhibits (Ghislaine, Prince Andrew, etc.)
- **Implementation:** CourtListener + extract embedded images from PDFs

### 6. Non-Prosecution Agreement Documents (2008)
**Source:** Miami Herald FOIA lawsuit
- **Contains:** Epstein's 2008 NPA with SDFL, victim statements, investigative records
- **Access:** Available through Crime Victims' Rights lawsuit documents
- **Implementation:** Search CourtListener for "Crime Victims Rights Act" + "Epstein"

### 7. U.S. Virgin Islands Lawsuit Documents
**Case:** Government of USVI v. Epstein Estate
- **Contains:** Estate records, property deeds, employee testimony, financial transactions
- **Status:** Ongoing litigation with continuous document releases
- **Implementation:** Already downloading via CourtListener (JPMorgan Chase case includes USVI docs)

### 8. Prince Andrew / Royal Family Documents
**Sources:**
- **Giuffre v. Prince Andrew Settlement:** Public filings (SDNY)
- **UK Court Documents:** If any publicly available
- **Photo Evidence:** Famous picture with Ghislaine Maxwell
- **Implementation:** Search CourtListener "Giuffre v. Andrew" + extract image exhibits

### 9. Les Wexner / Victoria's Secret Connection
**Sources:**
- **Civil Lawsuits:** Any cases mentioning Wexner-Epstein relationship
- **Corporate Records:** If publicly filed
- **Model Victim Statements:** Court testimony from VS models
- **Implementation:** Keyword search CourtListener: "Wexner", "Victoria's Secret", "Epstein"

### 10. Intelligence Agency Connections (Mossad/CIA Allegations)
**Public Sources:**
- **Whitney Webb Investigations:** Citations link to court docs and FOIA releases
- **Maria Farmer FBI Statements:** Filed in court cases
- **Robert Maxwell Connection:** Ghislaine's father ties to intelligence
- **Ari Ben-Menashe Claims:** Testimony from intelligence operative (verify if court filed)
- **Implementation:** 
  - Search CourtListener for "Mossad", "intelligence", "Maxwell Robert"
  - FBI Vault for any intelligence-related redacted documents

### 11. Financial Records & Shell Companies
**Sources:**
- **Paradise Papers / Panama Papers:** If Epstein entities mentioned
- **Court-Submitted Bank Records:** JPMorgan case exhibits
- **Trust Documents:** Submitted in estate litigation
- **Implementation:** Extract financial exhibits from existing JPMorgan USVI case downloads

### 12. Jean-Luc Brunel Documents
**Sources:**
- **French Court Documents:** If publicly available (Brunel died in French prison)
- **Model Agency Records:** MC2 modeling agency victim statements
- **U.S. Court References:** Any depositions mentioning Brunel
- **Implementation:** Search CourtListener "Brunel", check French court FOIA equivalents

### 13. Alan Dershowitz Documents
**Sources:**
- **Giuffre v. Dershowitz Defamation:** Court filings and exhibits
- **Email Evidence:** Submitted in various Epstein cases
- **Implementation:** CourtListener search "Dershowitz" + "Epstein"

### 14. Bill Clinton Connection Documents
**Sources:**
- **Flight Log Evidence:** Clinton trips on Lolita Express
- **Deposition References:** Witness statements mentioning Clinton
- **Secret Service Records:** If obtained through FOIA
- **Implementation:** Search existing docs for "Clinton", extract flight logs

### 15. Donald Trump Connection Documents
**Sources:**
- **1997 Rape Lawsuit (Katie Johnson):** Public filings before withdrawal
- **Deposition References:** Witness statements mentioning Trump
- **Photo Evidence:** Trump-Epstein party photos submitted as exhibits
- **Mar-a-Lago Employment Records:** If in court filings
- **Implementation:** Search existing docs for "Trump", "Mar-a-Lago"

---

## 🔧 IMPLEMENTATION STRATEGY

### Phase 1: FBI Vault Scraper
```python
# Create fbi_vault_scraper.py
- Navigate to https://vault.fbi.gov/jeffrey-epstein
- Download all PDF parts
- Extract text and add to documents.json
```

### Phase 2: DOJ Press Release Scraper
```python
# Create doj_scraper.py
- Search DOJ SDNY/SDFL for "Epstein" press releases
- Extract linked PDF documents
- Add to database
```

### Phase 3: Archive.org Flight Logs
```python
# Create flight_log_downloader.py
- Download from Internet Archive
- Parse flight manifests
- Make searchable
```

### Phase 4: Image Extraction from PDFs
```python
# Modify process_all_pdfs.py
- Extract embedded images from court documents
- Save photos separately
- Create image search functionality
```

### Phase 5: Expand CourtListener Searches
```python
# Modify download_all_epstein.py
- Add search terms: "Wexner", "Brunel", "Dershowitz", "Clinton", "Trump", "Maxwell Robert", "intelligence"
- Re-run comprehensive download
```

---

## 📊 ESTIMATED DOCUMENT COUNTS

| Source | Estimated Docs | Priority |
|--------|---------------|----------|
| FBI Vault | 300-500 pages | HIGH |
| DOJ Releases | 100-200 docs | HIGH |
| Flight Logs | 50-100 pages | HIGH |
| Maxwell Trial | 500+ exhibits | MEDIUM (partially have) |
| USVI Lawsuit | 1000+ docs | MEDIUM (downloading) |
| Prince Andrew | 50-100 docs | MEDIUM |
| Image Exhibits | 200+ photos | MEDIUM |
| Intelligence Links | 50-100 docs | LOW (speculative) |
| Financial Records | 500+ pages | LOW (in JPMorgan docs) |

---

## ⚠️ LEGAL & ETHICAL CONSIDERATIONS

1. **Only Public Documents:** Ensure all sources are officially released/unsealed
2. **No Speculation:** Stick to court-filed evidence only
3. **Victim Privacy:** Redact personal info if needed (court docs usually pre-redacted)
4. **Factual Presentation:** Let documents speak for themselves
5. **Source Attribution:** Always link to original source (CourtListener, FBI Vault, etc.)

---

## 🎯 NEXT STEPS

1. ✅ Complete current CourtListener download (789 docs)
2. ✅ Process all PDFs to searchable JSON
3. 🔲 Create FBI Vault scraper
4. 🔲 Download Archive.org flight logs
5. 🔲 Extract images from existing PDFs
6. 🔲 Add DOJ press release scraper
7. 🔲 Expand search terms for Wexner, Brunel, Clinton, Trump, intelligence
8. 🔲 Create photo gallery section on website
9. 🔲 Add "Filter by Source" dropdown (FBI, Court, Flight Logs, etc.)
10. 🔲 Deploy updated database to GitHub Pages

---

**TOTAL ESTIMATED FINAL DATABASE SIZE:** 3,000-5,000 documents + 200+ images
