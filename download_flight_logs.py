"""
EPSTEIN FLIGHT LOGS DOWNLOADER
Downloads flight logs from Internet Archive
"""

import requests
import os

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'epstein_documents', 'flight_logs')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Known flight log sources
FLIGHT_LOG_URLS = [
    # Gawker release (2015)
    "https://assets.documentcloud.org/documents/1507315/epstein-flight-manifests.pdf",
    
    # Alternative sources if available
    # Add more as discovered
]

def download_flight_logs():
    """Download all available flight log PDFs"""
    
    print("=" * 70)
    print("EPSTEIN FLIGHT LOGS - DOWNLOAD")
    print("=" * 70)
    
    for idx, url in enumerate(FLIGHT_LOG_URLS, 1):
        try:
            print(f"\n[{idx}/{len(FLIGHT_LOG_URLS)}] Downloading from: {url}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Get filename from URL
            filename = url.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename = f"flight_logs_{idx}.pdf"
            
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            
            # Download with progress
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r   Progress: {percent:.1f}%", end='', flush=True)
            
            print(f"\n   ✅ Downloaded: {filename} ({downloaded:,} bytes)")
            
        except Exception as e:
            print(f"\n   ❌ Failed: {str(e)}")
            continue
    
    print("\n" + "=" * 70)
    print("✅ FLIGHT LOGS DOWNLOAD COMPLETE")
    print(f"📂 Files saved to: {DOWNLOAD_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    download_flight_logs()
