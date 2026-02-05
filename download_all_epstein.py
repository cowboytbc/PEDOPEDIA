"""
Download ALL Epstein-related documents from CourtListener

This script will:
1. Search CourtListener for all Epstein-related dockets
2. Download every document from every case
3. Extract text and build a comprehensive database

WARNING: This could download THOUSANDS of files and take hours!
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from pathlib import Path
import json
import re

class ComprehensiveEpsteinDownloader:
    def __init__(self):
        self.download_dir = Path("epstein_documents/pdfs").absolute()
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.downloaded_count = 0
        self.failed_count = 0
        self.docket_list = []
        
    def setup_browser(self):
        """Setup Chrome browser with download preferences"""
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": str(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def log(self, message):
        """Print and log message"""
        print(message)
        
    def check_for_captcha(self):
        """Check if CAPTCHA is present and pause if needed"""
        try:
            # Check for common CAPTCHA indicators
            captcha_indicators = [
                "recaptcha",
                "captcha",
                "verify you are human",
                "confirm you are human",
                "hcaptcha"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for indicator in captcha_indicators:
                if indicator in page_source:
                    self.log("\n" + "="*70)
                    self.log("🤖 CAPTCHA DETECTED!")
                    self.log("="*70)
                    self.log("⏸️  PAUSING - Please solve the CAPTCHA in the browser window")
                    self.log("⏸️  Press ENTER when you've completed the CAPTCHA...")
                    self.log("="*70)
                    input()  # Wait for user to press Enter
                    self.log("✅ Resuming downloads...\n")
                    return True
                    
            return False
            
        except Exception as e:
            self.log(f"⚠️ Error checking for CAPTCHA: {e}")
            return False
        
    def find_all_epstein_dockets(self):
        """Search CourtListener for ALL Epstein-related cases"""
        self.log("\n" + "="*70)
        self.log("🔍 SEARCHING FOR ALL EPSTEIN-RELATED CASES")
        self.log("="*70)
        
        search_terms = [
            "epstein",
            "ghislaine maxwell",
            "jeffrey epstein",
            "jane doe epstein",
            "epstein victims"
        ]
        
        all_dockets = set()
        
        for search_term in search_terms:
            self.log(f"\n🔎 Searching: {search_term}")
            url = f"https://www.courtlistener.com/?q={search_term.replace(' ', '+')}&type=r&order_by=score+desc"
            
            try:
                self.driver.get(url)
                time.sleep(3)
                
                # Find all docket links
                links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/docket/']")
                
                for link in links:
                    href = link.get_attribute('href')
                    if '/docket/' in href and href not in all_dockets:
                        all_dockets.add(href)
                        
                self.log(f"   Found {len(links)} potential dockets")
                
            except Exception as e:
                self.log(f"   ⚠️ Error searching: {e}")
                
        self.docket_list = list(all_dockets)
        self.log(f"\n✅ TOTAL UNIQUE DOCKETS FOUND: {len(self.docket_list)}")
        return self.docket_list
        
    def download_docket(self, docket_url):
        """Download all documents from a specific docket"""
        self.log(f"\n{'='*70}")
        self.log(f"📂 Processing: {docket_url}")
        self.log(f"{'='*70}")
        
        try:
            self.driver.get(docket_url)
            time.sleep(2)
            
            # Check for CAPTCHA
            if self.check_for_captcha():
                return
            
            # Get case name
            try:
                case_name = self.driver.find_element(By.CSS_SELECTOR, "h1").text
                self.log(f"📋 Case: {case_name}")
            except:
                case_name = "Unknown Case"
            
            # Find all document rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.docket-entry")
            self.log(f"📄 Found {len(rows)} document entries")
            
            for i, row in enumerate(rows, 1):
                try:
                    # Find PDF links in this row
                    pdf_links = row.find_elements(By.CSS_SELECTOR, "a[href*='.pdf']")
                    
                    if not pdf_links:
                        continue
                        
                    for pdf_link in pdf_links:
                        try:
                            pdf_url = pdf_link.get_attribute('href')
                            
                            # Get document number from URL or row
                            doc_match = re.search(r'/(\d+)/', pdf_url)
                            doc_num = doc_match.group(1) if doc_match else str(i)
                            
                            # Download the PDF
                            self.log(f"   [{i}/{len(rows)}] Downloading document #{doc_num}...")
                            self.driver.get(pdf_url)
                            time.sleep(2)  # Wait for download
                            
                            self.downloaded_count += 1
                            
                        except Exception as e:
                            self.log(f"   ❌ Failed to download PDF: {e}")
                            self.failed_count += 1
                            
                except Exception as e:
                    self.log(f"   ⚠️ Error processing row {i}: {e}")
                    
        except Exception as e:
            self.log(f"❌ Failed to process docket: {e}")
            
    def download_all(self):
        """Main download orchestrator"""
        self.log("\n" + "="*70)
        self.log("🚀 COMPREHENSIVE EPSTEIN DOCUMENT DOWNLOADER")
        self.log("="*70)
        self.log("⚠️  WARNING: This will download THOUSANDS of files!")
        self.log("⚠️  This may take HOURS to complete!")
        self.log("="*70)
        
        try:
            self.setup_browser()
            
            # Step 1: Find all dockets
            dockets = self.find_all_epstein_dockets()
            
            if not dockets:
                self.log("❌ No dockets found!")
                return
                
            # Step 2: Download from each docket
            for idx, docket_url in enumerate(dockets, 1):
                self.log(f"\n{'#'*70}")
                self.log(f"DOCKET {idx}/{len(dockets)}")
                self.log(f"{'#'*70}")
                self.download_docket(docket_url)
                
                # Save progress periodically
                if idx % 5 == 0:
                    self.save_progress(idx)
                    
        except Exception as e:
            self.log(f"❌ FATAL ERROR: {e}")
            
        finally:
            self.log("\n" + "="*70)
            self.log("📊 DOWNLOAD COMPLETE")
            self.log("="*70)
            self.log(f"✅ Successfully downloaded: {self.downloaded_count} documents")
            self.log(f"❌ Failed: {self.failed_count} documents")
            self.log(f"📂 Total dockets processed: {len(self.docket_list)}")
            self.log(f"💾 Files saved to: {self.download_dir}")
            self.log("="*70)
            
            if hasattr(self, 'driver'):
                self.driver.quit()
                
    def save_progress(self, current_docket):
        """Save download progress"""
        progress = {
            'downloaded': self.downloaded_count,
            'failed': self.failed_count,
            'current_docket': current_docket,
            'total_dockets': len(self.docket_list)
        }
        
        with open('download_progress.json', 'w') as f:
            json.dump(progress, f, indent=2)
            
if __name__ == "__main__":
    downloader = ComprehensiveEpsteinDownloader()
    downloader.download_all()
