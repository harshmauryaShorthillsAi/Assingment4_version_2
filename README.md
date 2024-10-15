# Assignment-3 Python
   ## Overview
- The data_extractor directory houses a set of tools specifically designed to extract data from various file formats and efficiently store the resulting information.

#project Structure

  Assignment4_version_2
│
├── Data_extractor
│   ├── docx_extractor.py
│   ├── pdf_extractor.py
│   ├── ppt_extractor.py
│   └── extractor.py
│
├── File_loaders
│   ├── docx_loader.py
│   ├── file_loader.py
│   ├── pdf_loader.py
│   └── ppt_loader.py
│
├── Storage
│   ├── file_storage.py
│   ├── sql_storage.py
│   └── storage.py
│
├── tests
│   └── test_extractor.py
│
├── Extracted_data
│
├── Files
│   └── containfiles
│
├── Test_files
│   ├── Docx
│   ├── Pdf
│   └── pptx
│
├── main.py
└── requirements.txt


## How to Use
- To begin, clone the repository and set the file_path variable to the location of the main file. Afterward, run the main.py script to initiate the data extraction process.

# Loaders
- The data_extractor directory features the following loaders, which facilitate data extraction from various file types:

PDFLoader: Extracts data from PDF files.
DOCXLoader: Extracts data from DOCX files.
PPTLoader: Extracts data from PPTX files.
Data Extraction
The data_extractor leverages the specified loaders to collect data from supported file formats, providing a unified interface for accessing the extracted information.

# Storage Options
The data_extractor directory offers the following storage solutions for managing the extracted data:

FileStorage: Saves the extracted data in a file.
SQLStorage: Saves the extracted data in a SQL database.
Functionality
The data_extractor offers the following features:

Extracts data from PDF, DOCX, and PPTX files using the appropriate loaders.
Saves the extracted data either in a file or in a SQL database using the provided storage options.
Provides a unified interface for easy access to the extracted data.
# Purpose
The main goal of the data_extractor directory is to deliver a user-friendly and efficient method for extracting data from a variety of file formats and storing that data for subsequent analysis or processing.
