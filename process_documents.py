"""
Epstein Files Document Processor

This Python script helps you extract text from PDF documents and format them
for the Epstein Files Search tool. It processes PDFs and generates JSON entries
that can be added to documents.json.

Requirements:
    pip install pdfplumber

Usage:
    python process_documents.py path/to/document.pdf
"""

import pdfplumber
import json
import sys
import os
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {page_num} ---\n{text}"
            return full_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def create_document_entry(pdf_path, title=None, source=None, date=None):
    """Create a JSON document entry from a PDF file."""
    
    # Extract text
    content = extract_text_from_pdf(pdf_path)
    if not content:
        return None
    
    # Get filename as default title
    if not title:
        title = os.path.basename(pdf_path).replace('.pdf', '')
    
    # Create document entry
    doc_entry = {
        "id": 0,  # User should update this
        "title": title,
        "source": source or "Unknown - Please add source information",
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "page": "Multiple",
        "content": content.strip()
    }
    
    return doc_entry

def process_pdf(pdf_path):
    """Process a PDF and output JSON for documents.json."""
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return
    
    print(f"Processing: {pdf_path}")
    print("Extracting text...")
    
    # Get document details from user
    title = input("Enter document title (or press Enter to use filename): ").strip()
    source = input("Enter source (case number, exhibit, etc.): ").strip()
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    
    # Create document entry
    doc_entry = create_document_entry(pdf_path, title, source, date)
    
    if doc_entry:
        # Output JSON
        output_file = pdf_path.replace('.pdf', '_extracted.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(doc_entry, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Success! JSON saved to: {output_file}")
        print("\nNext steps:")
        print("1. Open the generated JSON file and review the extracted text")
        print("2. Update the 'id' field to be unique")
        print("3. Copy the JSON entry into documents.json")
        print("4. Update 'lastUpdated' field in documents.json")
        
        # Show preview
        print("\n--- Preview (first 500 characters) ---")
        print(doc_entry['content'][:500] + "...")
    else:
        print("Failed to process document")

def batch_process(directory):
    """Process all PDFs in a directory."""
    
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return
    
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    all_entries = []
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(directory, pdf_file)
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file}")
        
        title = input("Title (Enter to use filename): ").strip() or pdf_file.replace('.pdf', '')
        source = input("Source: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        
        doc_entry = create_document_entry(pdf_path, title, source, date)
        if doc_entry:
            doc_entry['id'] = i
            all_entries.append(doc_entry)
            print("✓ Added")
    
    # Save all entries
    output_file = os.path.join(directory, 'batch_extracted.json')
    output_data = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "documents": all_entries
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Batch complete! All documents saved to: {output_file}")
    print("You can now copy the 'documents' array into your main documents.json file")

def main():
    """Main function."""
    
    print("=" * 60)
    print("Epstein Files Document Processor")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isdir(path):
            batch_process(path)
        else:
            process_pdf(path)
    else:
        print("\nUsage:")
        print("  Single file: python process_documents.py document.pdf")
        print("  Batch:       python process_documents.py /path/to/pdfs/")
        print("\nOr run without arguments for interactive mode:")
        
        mode = input("\nEnter 's' for single file or 'b' for batch: ").lower()
        
        if mode == 's':
            pdf_path = input("Enter PDF file path: ").strip()
            process_pdf(pdf_path)
        elif mode == 'b':
            directory = input("Enter directory path: ").strip()
            batch_process(directory)
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
