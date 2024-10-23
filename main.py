




import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from data_extractor.data_extractor.extractor import FileExtractor
from data_extractor.file_loaders.loader import UnifiedFileLoader  # Import the unified loader
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage

def main():
    # Create a Tkinter root window (it won't be shown)
    root = Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog and allow selection of PDF, DOCX, and PPTX files
    file_path = askopenfilename(
        title="Select a file",
        filetypes=[("PDF files", "*.pdf"),
                   ("Word files", "*.docx"),
                   ("PowerPoint files", "*.pptx"),
                   ("PowerPoint files", "*.ppt")])  # Added PPT option for compatibility
    if not file_path:
        print("No file selected. Exiting.")
        return

    # Use the UnifiedFileLoader to load the file
    loader = UnifiedFileLoader()

    # Determine the file type
    if file_path.endswith(".pdf"):
        file_type = "pdf"
    elif file_path.endswith(".docx"):
        file_type = "docx"
    elif file_path.endswith(".pptx") or file_path.endswith(".ppt"):
        file_type = "pptx"
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")

    # Use the FileExtractor with the unified loader
    extractor = FileExtractor(loader, file_type)

    # Load the selected file
    extractor.load(file_path)

    # Extract text
    extracted_text = extractor.extract_text()

    # Extract images (if available)
    images = extractor.extract_images()

    # Extract URLs (if available)
    urls = extractor.extract_urls()

    # Extract tables (if available)
    tables = extractor.extract_tables()

    # Create a folder for storing the extracted data
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join("extracted_data", base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted text
    file_storage.store(extracted_text, os.path.basename(file_path), 'text')

    # Save the extracted images
    if images:
        file_storage.store(images, os.path.basename(file_path), 'image')

    # Save the extracted URLs (if any)
    if urls:
        file_storage.store(urls, os.path.basename(file_path), 'url')

    # Save the extracted tables (if any)
    if tables:
        file_storage.store(tables, os.path.basename(file_path), 'table')

    print(f"Extracted data saved to: {output_dir}")

    # Create an instance of SQLStorage
    sql_storage = SQLStorage("assignment4.db")

    # Store the extracted text in the SQL database
    sql_storage.store("text", extracted_text)

    # Store the extracted images in the SQL database
    if images:
        sql_storage.store("image", images)

    # Store the extracted URLs in the SQL database
    if urls:
        sql_storage.store("url", urls)

    # Store the extracted tables in the SQL database
    if tables:
        for table in tables:
            sql_storage.store("data_table", table)

    print("Data stored in SQL database")
    sql_storage.close()

if __name__ == "__main__":
    main()
