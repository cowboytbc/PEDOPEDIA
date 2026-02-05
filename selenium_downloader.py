"""
Browser-Based Epstein Document Downloader
Uses Selenium to automate downloading ALL documents like a real browser

Requirements:
    pip install selenium webdriver-manager

Usage:
    python selenium_downloader.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from pathlib import Path
import json
from datetime import datetime

class BrowserDocumentDownloader:
    def __init__(self, output_dir="epstein_documents"):
        self.output_dir = Path(output_dir)
        self.pdfs_dir = self.output_dir / "pdfs"
        self.pdfs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": str(self.pdfs_dir.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        
        # Keep browser visible so you can see progress
        # chrome_options.add_argument("--headless")  # Uncomment to hide browser
        
        print("🌐 Starting Chrome browser...")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        self.downloaded_count = 0
        self.log_file = self.output_dir / "download_log.txt"
    
    def log(self, message):
        """Log to file and console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def download_giuffre_maxwell(self):
        """Download all documents from Giuffre v. Maxwell case"""
        url = "https://www.courtlistener.com/docket/4355308/giuffre-v-maxwell/"
        
        self.log(f"Opening case: {url}")
        self.driver.get(url)
        time.sleep(3)  # Let page load
        
        # Find all document links
        self.log("Scanning for document links...")
        
        try:
            # Find all PDF download links
            pdf_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/pdf/']")
            
            if not pdf_links:
                # Try alternative selectors
                pdf_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Download PDF")
            
            total_docs = len(pdf_links)
            self.log(f"Found {total_docs} document links")
            
            if total_docs == 0:
                self.log("⚠️  No document links found. The page structure may have changed.")
                self.log("Trying to find all links on the page...")
                
                # Get all links and filter for documents
                all_links = self.driver.find_elements(By.TAG_NAME, "a")
                pdf_links = [link for link in all_links if '/recap/' in link.get_attribute('href') or '.pdf' in link.get_attribute('href')]
                total_docs = len(pdf_links)
                self.log(f"Found {total_docs} potential document links")
            
            # Download each document
            for i, link in enumerate(pdf_links, 1):
                try:
                    href = link.get_attribute('href')
                    text = link.text
                    
                    self.log(f"\n[{i}/{total_docs}] Downloading: {text[:60]}")
                    self.log(f"  URL: {href}")
                    
                    # Open in new tab
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    
                    # Navigate to document
                    self.driver.get(href)
                    time.sleep(2)  # Wait for download
                    
                    # Close tab and switch back
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    
                    self.downloaded_count += 1
                    self.log(f"  ✅ Downloaded ({self.downloaded_count} total)")
                    
                    # Be nice to the server
                    time.sleep(1)
                    
                    # Every 10 documents, take a longer break
                    if i % 10 == 0:
                        self.log(f"  💾 Progress: {i}/{total_docs} documents processed")
                        time.sleep(3)
                    
                except Exception as e:
                    self.log(f"  ❌ Error: {e}")
                    # Try to get back to main window
                    try:
                        if len(self.driver.window_handles) > 1:
                            self.driver.switch_to.window(self.driver.window_handles[0])
                    except:
                        pass
                    continue
            
            self.log(f"\n✅ Giuffre v. Maxwell complete: {self.downloaded_count} documents")
            
        except Exception as e:
            self.log(f"❌ Error scanning page: {e}")
    
    def download_all(self):
        """Download from all major cases"""
        self.log("="*60)
        self.log("🚀 EPSTEIN DOCUMENT AUTOMATIC DOWNLOADER")
        self.log("="*60)
        self.log(f"Download directory: {self.pdfs_dir.absolute()}")
        
        try:
            # Main case with most documents
            self.download_giuffre_maxwell()
            
            # Could add more cases here
            
        except Exception as e:
            self.log(f"❌ Fatal error: {e}")
        
        finally:
            self.log("\n" + "="*60)
            self.log(f"✅ COMPLETE: Downloaded {self.downloaded_count} documents")
            self.log("="*60)
            self.log(f"PDFs saved to: {self.pdfs_dir.absolute()}")
            self.log(f"Log saved to: {self.log_file.absolute()}")
            
            input("\nPress Enter to close browser and continue...")
            self.driver.quit()

def main():
    print("\n⚖️  AUTOMATED EPSTEIN DOCUMENT DOWNLOADER")
    print("="*60)
    print("This uses browser automation to download ALL documents")
    print("You'll see Chrome open and automatically download files")
    print("="*60)
    
    response = input("\nReady to start? (Press Enter to continue, Ctrl+C to cancel): ")
    
    downloader = BrowserDocumentDownloader()
    
    try:
        downloader.download_all()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        downloader.driver.quit()
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        try:
            downloader.driver.quit()
        except:
            pass
    
    print("\n🎉 Next steps:")
    print("1. Check the epstein_documents/pdfs/ folder")
    print("2. Run: python process_all_pdfs.py")
    print("3. Then open index.html to search!")

if __name__ == "__main__":
    main()
