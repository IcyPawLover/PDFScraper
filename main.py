import os
import glob
import csv
import pdfplumber
from handlers.config_handler import get_config
from handlers.logging_handler import get_logger

# Initialize logger
logger = get_logger('pdf_to_csv.log', print_log_messages=True)

# Configuration setup
config_path = 'config.ini'
config = get_config(config_path, logger)

# Read configuration for the PDF directory path and start page
pdf_directory_path = config.read_config('Paths', 'PDFDirectoryPath')
start_page = int(config.read_config('Paths', 'StartPage')) - 1  # Adjusting for zero-based index

def scrape_pdf_directory_to_csv(pdf_dir_path, start_page):
    """
    Function to scrape text from PDF files in a directory, starting from a specific page, and write data to CSV files.
    """
    logger.info(f"Searching for PDF files in directory: {pdf_dir_path}")
    pdf_files = glob.glob(os.path.join(pdf_dir_path, '*.pdf'))
    
    if not pdf_files:
        logger.info("No PDF files found in the specified directory.")
        return
    
    for pdf_path in pdf_files:
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]
        csv_file_path = os.path.join(pdf_dir_path, f"{file_name}.csv")
        
        logger.info(f"Processing PDF file: {pdf_path}")
        
        with pdfplumber.open(pdf_path) as pdf, open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for page in pdf.pages[start_page:]:  # Start processing from the configured page
                text = page.extract_text()
                if text:  # Check if text was extracted to avoid errors
                    for line in text.split('\n'):
                        csv_writer.writerow([line])
        
        logger.info(f"Successfully wrote extracted data to CSV: {csv_file_path}")

# Execute the process for the specified directory with the start page
scrape_pdf_directory_to_csv(pdf_directory_path, start_page)
