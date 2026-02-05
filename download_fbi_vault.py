"""
FBI VAULT EPSTEIN DOCUMENT DOWNLOADER
Downloads all Jeffrey Epstein investigation files from FBI Vault
https://vault.fbi.gov/jeffrey-epstein
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# Download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'epstein_documents', 'fbi_vault')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def setup_driver():
    """Configure Chrome driver with download settings"""
    chrome_options = webdriver.ChromeOptions()
    
    prefs = {
        'download.default_directory': DOWNLOAD_DIR,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True
    }
    chrome_options.add_experimental_option('prefs', prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def download_fbi_vault_documents():
    """
    Navigate to FBI Vault Epstein page and download all PDF parts
    """
    driver = setup_driver()
    
    try:
        print("=" * 70)
        print("FBI VAULT - JEFFREY EPSTEIN DOCUMENT DOWNLOAD")
        print("=" * 70)
        
        # Navigate to FBI Vault Epstein page
        url = "https://vault.fbi.gov/jeffrey-epstein"
        print(f"\n🔍 Navigating to {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Find all PDF links (FBI Vault uses specific structure)
        # Example: vault.fbi.gov/jeffrey-epstein/Jeffrey%20Epstein%20Part%2001%20of%2022/view
        
        pdf_links = []
        
        # Method 1: Look for links containing "Part" or ".pdf"
        all_links = driver.find_elements(By.TAG_NAME, "a")
        
        for link in all_links:
            href = link.get_attribute('href')
            if href and ('part' in href.lower() or '.pdf' in href.lower() or '/view' in href.lower()):
                if 'epstein' in href.lower():
                    pdf_links.append(href)
        
        # Remove duplicates
        pdf_links = list(set(pdf_links))
        
        print(f"\n📄 Found {len(pdf_links)} potential PDF documents")
        
        if not pdf_links:
            print("⚠️  No PDFs found automatically. Checking page structure...")
            
            # Try alternative method: look for download buttons
            download_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Download')]")
            for btn in download_buttons:
                href = btn.get_attribute('href')
                if href:
                    pdf_links.append(href)
        
        # Download each PDF
        for idx, pdf_url in enumerate(pdf_links, 1):
            try:
                print(f"\n[{idx}/{len(pdf_links)}] Downloading: {pdf_url}")
                
                # If URL ends with /view, convert to download
                if '/view' in pdf_url:
                    pdf_url = pdf_url.replace('/view', '/download')
                
                # Navigate to PDF or download directly
                if pdf_url.endswith('.pdf'):
                    # Direct PDF link - download with requests
                    response = requests.get(pdf_url, stream=True)
                    filename = pdf_url.split('/')[-1]
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"   ✅ Downloaded: {filename}")
                else:
                    # Navigate and let browser download
                    driver.get(pdf_url)
                    time.sleep(3)  # Wait for download to start
                    print(f"   ✅ Download initiated")
                
            except Exception as e:
                print(f"   ❌ Failed: {str(e)}")
                continue
        
        print("\n" + "=" * 70)
        print("✅ FBI VAULT DOWNLOAD COMPLETE")
        print(f"📂 Files saved to: {DOWNLOAD_DIR}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()

if __name__ == "__main__":
    download_fbi_vault_documents()
