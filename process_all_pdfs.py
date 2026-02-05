"""
Batch PDF Text Extractor for Epstein Documents

Processes all downloaded PDFs and creates a complete documents.json database.

Requirements:
    pip install pdfplumber

Usage:
    python process_all_pdfs.py
"""

import pdfplumber
import json
import os
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n"
            return full_text.strip()
    except Exception as e:
        print(f"❌ Error extracting {pdf_path.name}: {e}")
        return None

def parse_filename(filename):
    """Parse information from filename"""
    # Format: CaseName_EntryNum_Description.pdf
    parts = filename.replace('.pdf', '').split('_', 2)
    
    case_name = parts[0].replace('_', ' ') if len(parts) > 0 else "Unknown Case"
    entry_num = parts[1] if len(parts) > 1 else "N/A"
    description = parts[2] if len(parts) > 2 else "Document"
    
    return case_name, entry_num, description

def process_all_pdfs(pdfs_dir="epstein_documents/pdfs", output_file="documents.json"):
    """Process all PDFs and create documents.json"""
    
    pdfs_path = Path(pdfs_dir)
    
    if not pdfs_path.exists():
        print(f"❌ Directory not found: {pdfs_path}")
        print("Run download_all_documents.py first!")
        return
    
    # Find all PDFs
    pdf_files = list(pdfs_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdfs_path}")
        return
    
    print(f"\n📚 Found {len(pdf_files)} PDF files")
    print("🔄 Extracting text from all documents...")
    print("(This may take a while)\n")
    
    documents = []
    failed = []
    
    # Process each PDF
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing: {pdf_file.name[:60]}...")
        
        # Extract text
        content = extract_text_from_pdf(pdf_file)
        
        if content:
            # Parse filename for metadata
            case_name, entry_num, description = parse_filename(pdf_file.name)
            
            # Create document entry
            doc_entry = {
                "id": i,
                "title": description,
                "source": f"{case_name} - Entry #{entry_num}",
                "date": "Various",  # Could parse from content if needed
                "page": "Multiple",
                "content": content,
                "filename": pdf_file.name
            }
            
            documents.append(doc_entry)
            print(f"   ✅ Extracted {len(content)} characters")
        else:
            failed.append(pdf_file.name)
            print(f"   ⚠️  Failed to extract text")
    
    # Create final JSON structure
    output_data = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "totalDocuments": len(documents),
        "source": "Official court documents from CourtListener.com",
        "disclaimer": "All documents are publicly available official court records",
        "documents": documents
    }
    
    # Save to JSON
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*60)
    print("✅ PROCESSING COMPLETE")
    print("="*60)
    print(f"Successfully processed: {len(documents)} documents")
    print(f"Failed: {len(failed)} documents")
    print(f"\nOutput saved to: {output_path.absolute()}")
    
    if failed:
        print("\n⚠️  Failed files:")
        for f in failed:
            print(f"   - {f}")
    
    # Save failed list
    if failed:
        failed_log = Path("epstein_documents/failed_extractions.txt")
        with open(failed_log, 'w') as f:
            f.write("Files that failed text extraction:\n\n")
            for filename in failed:
                f.write(f"{filename}\n")
        print(f"\nFailed files logged to: {failed_log.absolute()}")
    
    print(f"\n🎉 Your search tool is now ready!")
    print(f"   Open index.html in your browser to search all {len(documents)} documents")
    
    # Generate statistics
    generate_statistics(documents)

def generate_statistics(documents):
    """Generate statistics about the document collection"""
    stats_file = Path("epstein_documents/STATISTICS.txt")
    
    # Count by case
    by_case = {}
    total_chars = 0
    
    for doc in documents:
        case = doc['source'].split(' - ')[0] if ' - ' in doc['source'] else "Unknown"
        if case not in by_case:
            by_case[case] = 0
        by_case[case] += 1
        total_chars += len(doc['content'])
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("DOCUMENT COLLECTION STATISTICS\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total Documents: {len(documents)}\n")
        f.write(f"Total Characters: {total_chars:,}\n")
        f.write(f"Average per Document: {total_chars // len(documents):,} characters\n\n")
        
        f.write("Documents by Case:\n")
        f.write("-"*40 + "\n")
        for case, count in sorted(by_case.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{case}: {count} documents\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("This database contains only official, publicly released\n")
        f.write("court documents from verified sources.\n")
    
    print(f"\n📊 Statistics saved to: {stats_file.absolute()}")

def main():
    """Main function"""
    print("\n📄 EPSTEIN DOCUMENTS - TEXT EXTRACTION")
    print("="*60)
    print("Processing all downloaded PDFs...")
    print("="*60)
    
    # Check for tqdm
    try:
        from tqdm import tqdm
        print("✅ Using tqdm for progress bars")
    except ImportError:
        print("⚠️  Install tqdm for better progress tracking: pip install tqdm")
    
    process_all_pdfs()

if __name__ == "__main__":
    main()
