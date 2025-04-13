import PyPDF2
import os
import logging
import traceback

# Configure logging
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    logger.debug(f"Starting PDF extraction for file: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
    text = ""
    try:
        logger.debug("Opening PDF file")
        with open(pdf_path, 'rb') as file:
            logger.debug("Creating PDF reader")
            pdf_reader = PyPDF2.PdfReader(file)
            
            if len(pdf_reader.pages) == 0:
                logger.error("PDF file is empty")
                raise ValueError("PDF file is empty")
                
            logger.debug(f"Processing {len(pdf_reader.pages)} pages")
            for i, page in enumerate(pdf_reader.pages, 1):
                logger.debug(f"Extracting text from page {i}")
                page_text = page.extract_text()
                text += page_text + "\n"
                logger.debug(f"Page {i} extracted {len(page_text)} characters")
                
        if not text.strip():
            logger.error("No text could be extracted from the PDF")
            raise ValueError("No text could be extracted from the PDF")
            
        logger.debug(f"Successfully extracted {len(text)} total characters")
        return text
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}\n{traceback.format_exc()}")
        raise Exception(f"Error processing PDF: {str(e)}") 