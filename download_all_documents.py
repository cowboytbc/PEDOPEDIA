"""
Automated Epstein Document Downloader
Downloads ALL publicly available Epstein court documents from CourtListener

This script uses the CourtListener API to systematically download all documents
from major Epstein-related cases.

Requirements:
    pip install requests pdfplumber tqdm

Usage:
    python download_all_documents.py
"""

import requests
import json
import os
import time
from pathlib import Path
from datetime import datetime

# CourtListener API (free, no key required for basic access)
BASE_URL = "https://www.courtlistener.com/api/rest/v3"

# Major Epstein-related dockets
EPSTEIN_DOCKETS = {
    "Giuffre v. Maxwell": {
        "docket_id": 4355308,
        "case_name": "giuffre-v-maxwell",
        "court": "nysd",
        "case_number": "1:15-cv-07433"
    },
    "United States v. Epstein (SDFL)": {
        "docket_id": None,  # Will search for it
        "case_name": "united-states-v-epstein",
        "court": "flsd", 
        "case_number": "1:08-cr-10435"
    },
    "United States v. Maxwell": {
        "docket_id": None,
        "case_name": "united-states-v-maxwell",
        "court": "nysd",
        "case_number": "1:20-cr-00330"
    }
}

class EpsteinDocumentDownloader:
    def __init__(self, output_dir="epstein_documents"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.pdfs_dir = self.output_dir / "pdfs"
        self.pdfs_dir.mkdir(exist_ok=True)
        
        self.json_dir = self.output_dir / "json"
        self.json_dir.mkdir(exist_ok=True)
        
        self.log_file = self.output_dir / "download_log.json"
        self.downloaded = self.load_log()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EpsteinDocumentResearch/1.0 (Educational Research)'
        })
    
    def load_log(self):
        """Load log of already downloaded documents"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {"documents": [], "last_updated": None}
    
    def save_log(self):
        """Save download log"""
        self.downloaded["last_updated"] = datetime.now().isoformat()
        with open(self.log_file, 'w') as f:
            json.dump(self.downloaded, f, indent=2)
    
    def search_dockets(self, search_term):
        """Search for dockets by term"""
        print(f"\n🔍 Searching for dockets: {search_term}")
        
        url = f"{BASE_URL}/dockets/"
        params = {
            'q': search_term,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                print(f"   Found {data.get('count', 0)} dockets")
                return data.get('results', [])
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
    
    def get_docket_entries(self, docket_id):
        """Get all entries for a specific docket"""
        print(f"\n📋 Fetching docket entries for docket ID: {docket_id}")
        print("   Using direct website scraping method...")
        
        # Use the website directly since API requires auth
        url = f"https://www.courtlistener.com/docket/{docket_id}/json/"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                entries = data.get('docket_entries', [])
                print(f"   ✅ Found {len(entries)} entries")
                return entries
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []
        
        all_entries = []
        page = 1
        
        while True:
            try:
                response = self.session.get(url, params=params, timeout=30)
                if response.status_code != 200:
                    print(f"   ⚠️  Status code: {response.status_code}")
                    break
                
                data = response.json()
                results = data.get('results', [])
                all_entries.extend(results)
                
                print(f"   Page {page}: {len(results)} entries")
                
                # Check for next page
                if not data.get('next'):
                    break
                
                url = data['next']
                page += 1
                time.sleep(0.5)  # Be nice to the API
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                break
        
        print(f"   ✅ Total entries: {len(all_entries)}")
        return all_entries
    
    def get_recap_documents(self, entry):
        """Get RECAP documents from a docket entry"""
        # Documents are embedded in the entry structure
        recap_docs = entry.get('recap_documents', [])
        return recap_docs
    
    def download_document(self, doc_info, case_name):
        """Download a single document"""
        doc_id = doc_info.get('id')
        
        # Check if already downloaded
        if any(d['id'] == doc_id for d in self.downloaded['documents']):
            return False
        
        filepath = doc_info.get('filepath_local')
        if not filepath:
            return False
        
        # Build download URL
        download_url = f"https://www.courtlistener.com{filepath}"
        
        # Create filename
        entry_num = doc_info.get('document_number', 'unknown')
        description = doc_info.get('description', 'document')
        safe_desc = "".join(c for c in description if c.isalnum() or c in (' ', '-', '_'))[:50]
        filename = f"{case_name}_{entry_num}_{safe_desc}.pdf"
        output_path = self.pdfs_dir / filename
        
        try:
            print(f"      📥 Downloading: {filename}")
            response = self.session.get(download_url, timeout=60, stream=True)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Log successful download
                self.downloaded['documents'].append({
                    'id': doc_id,
                    'filename': filename,
                    'case': case_name,
                    'entry_number': entry_num,
                    'description': description,
                    'downloaded_at': datetime.now().isoformat()
                })
                self.save_log()
                
                print(f"      ✅ Saved: {filename}")
                return True
            else:
                print(f"      ⚠️  Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
            return False
    
    def download_case(self, case_name, docket_id):
        """Download all documents for a specific case"""
        print(f"\n{'='*60}")
        print(f"📁 CASE: {case_name}")
        print(f"{'='*60}")
        
        # Get all docket entries
        entries = self.get_docket_entries(docket_id)
        
        if not entries:
            print("   ⚠️  No entries found")
            return
        
        total_downloaded = 0
        
        # Process each entry
        for i, entry in enumerate(entries, 1):
            entry_num = entry.get('entry_number', 'N/A')
            description = entry.get('description', 'No description')
            
            print(f"\n   [{i}/{len(entries)}] Entry #{entry_num}: {description[:60]}")
            
            # Get documents for this entry
            documents = self.get_recap_documents(entry)
            
            if documents:
                print(f"      Found {len(documents)} document(s)")
                for doc in documents:
                    if self.download_document(doc, case_name.replace(' ', '_')):
                        total_downloaded += 1
                    time.sleep(0.3)  # Be respectful to the server
            
            # Periodic save
            if i % 10 == 0:
                self.save_log()
                print(f"\n   💾 Progress saved ({total_downloaded} documents downloaded)")
        
        print(f"\n✅ {case_name}: Downloaded {total_downloaded} new documents")
    
    def download_all(self):
        """Download documents from all major Epstein cases"""
        print("\n" + "="*60)
        print("🚀 EPSTEIN DOCUMENT MASS DOWNLOADER")
        print("="*60)
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Previously downloaded: {len(self.downloaded['documents'])} documents")
        
        # Download from known dockets
        for case_name, info in EPSTEIN_DOCKETS.items():
            docket_id = info.get('docket_id')
            
            if docket_id:
                self.download_case(case_name, docket_id)
            else:
                # Search for the docket
                print(f"\n🔍 Searching for: {case_name}")
                results = self.search_dockets(info['case_name'])
                
                if results:
                    # Use first result
                    docket_id = results[0].get('id')
                    if docket_id:
                        self.download_case(case_name, docket_id)
            
            time.sleep(1)  # Pause between cases
        
        # Final summary
        print("\n" + "="*60)
        print("✅ DOWNLOAD COMPLETE")
        print("="*60)
        print(f"Total documents downloaded: {len(self.downloaded['documents'])}")
        print(f"PDFs saved to: {self.pdfs_dir.absolute()}")
        print(f"Log saved to: {self.log_file.absolute()}")
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate a summary of downloaded documents"""
        summary_file = self.output_dir / "DOWNLOAD_SUMMARY.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("EPSTEIN DOCUMENT DOWNLOAD SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Documents: {len(self.downloaded['documents'])}\n\n")
            
            # Group by case
            by_case = {}
            for doc in self.downloaded['documents']:
                case = doc['case']
                if case not in by_case:
                    by_case[case] = []
                by_case[case].append(doc)
            
            for case, docs in by_case.items():
                f.write(f"\n{case}\n")
                f.write("-" * len(case) + "\n")
                f.write(f"Documents: {len(docs)}\n\n")
                
                for doc in docs:
                    f.write(f"  [{doc['entry_number']}] {doc['description'][:60]}\n")
                    f.write(f"      File: {doc['filename']}\n")
                    f.write(f"      Downloaded: {doc['downloaded_at']}\n\n")
        
        print(f"\n📄 Summary saved to: {summary_file.absolute()}")

def main():
    """Main function"""
    print("\n⚖️  OFFICIAL EPSTEIN COURT DOCUMENTS DOWNLOADER")
    print("="*60)
    print("This tool downloads publicly available court documents")
    print("from CourtListener.com (Free Law Project)")
    print("="*60)
    
    input("\nPress Enter to start downloading ALL documents...")
    
    downloader = EpsteinDocumentDownloader()
    
    try:
        downloader.download_all()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        downloader.save_log()
        print("Progress has been saved. Run again to resume.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        downloader.save_log()
    
    print("\n🎉 Done! Next steps:")
    print("1. Run: python process_all_pdfs.py")
    print("2. This will extract text from all PDFs")
    print("3. Then populate your documents.json database")

if __name__ == "__main__":
    main()
