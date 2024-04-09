
# PDF to CSV Extractor

## Overview
This project provides a tool for extracting text from PDF files and saving the extracted text into CSV format. It is designed to process all PDF files within a specified directory, starting the text extraction from a user-configured page. This tool is particularly useful for converting large volumes of PDF documents into a more accessible and manageable format.

## Features
- **Bulk Processing:** Automatically processes all PDF files found in a specified directory.
- **Configurable Start Page:** Begins text extraction from a user-defined page number to skip irrelevant content.
- **Logging:** Includes detailed logging of the processing steps and outcomes, aiding in debugging and verification of the extraction process.

## Requirements
- Python 3.x
- pdfplumber
- A configuration file named `config.ini` for setting up the PDF directory path and start page.

## Installation
1. Ensure that Python 3 is installed on your system.
2. Install the required Python packages:
   ```
   pip install pdfplumber
   ```
3. Clone this repository to your local machine.

## Configuration
Before running the script, configure the `config.ini` file with the following parameters:
- `PDFDirectoryPath`: The path to the directory containing the PDF files to be processed.
- `StartPage`: The page number at which to start text extraction (1-indexed).

Example `config.ini`:
```ini
[Paths]
PDFDirectoryPath = path/to/your/pdf/directory
StartPage = 2
```

## Usage
To run the script, simply execute the following command in your terminal:
```
python main.py
```
Ensure that the `config.ini` file is in the same directory as `main.py`, or adjust the `config_path` variable in the script accordingly.

## Logging
The script generates a log file named `pdf_to_csv.log`, containing information about the processing of each PDF file. This includes messages about the start of processing, successful extractions, and any errors encountered. To view the log messages in the console as well, set `print_log_messages=True` in the `get_logger` function call.

## License
[MIT License](https://opensource.org/licenses/MIT)

## Contributing
Contributions to this project are welcome. Please submit a pull request or open an issue to suggest improvements or report bugs.
