# /// script
# dependencies = [
#   "pypdf"
# ]
# ///

from pypdf import PdfReader, PdfWriter
import os

def merge():
    downloads_path = r"C:\Users\HP\Downloads\reppppppppp.pdf"
    report_path = r"C:\Users\HP\.gemini\antigravity\scratch\patient_appointment_system\patient_appointment_system_report_v2.pdf"
    output_path = r"C:\Users\HP\.gemini\antigravity\scratch\patient_appointment_system\patient_appointment_system_report_v3.pdf"
    
    if not os.path.exists(downloads_path):
        print(f"Error: {downloads_path} not found.")
        return
        
    if not os.path.exists(report_path):
        print(f"Error: {report_path} not found.")
        return

    print(f"Reading {downloads_path}...")
    reader_source = PdfReader(downloads_path)
    print(f"Source PDF page count: {len(reader_source.pages)}")
    
    print(f"Reading {report_path}...")
    reader_report = PdfReader(report_path)
    print(f"Report PDF page count: {len(reader_report.pages)}")
    
    writer = PdfWriter()
    
    # Insert first 4 pages from downloads_path
    pages_to_add = min(4, len(reader_source.pages))
    print(f"Adding first {pages_to_add} pages from source...")
    for i in range(pages_to_add):
        writer.add_page(reader_source.pages[i])
        
    # Append all pages from the report
    print("Appending report pages...")
    for page in reader_report.pages:
        writer.add_page(page)
        
    print(f"Writing merged PDF to {output_path}...")
    try:
        with open(output_path, "wb") as f:
            writer.write(f)
        print("Success: Merger completed successfully!")
    except Exception as e:
        print(f"Error writing to output: {str(e)}")

if __name__ == "__main__":
    merge()
