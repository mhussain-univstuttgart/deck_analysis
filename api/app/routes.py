from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import traceback
import logging
from ..utils.pdf_utils import extract_text_from_pdf
from ..utils.ai_utils import analyze_differences

main_bp = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        logger.debug("Starting file upload process")
        
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        logger.debug(f"Received file: {file.filename}")
        
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400
            
        # Ensure upload directory exists
        upload_dir = current_app.config['UPLOAD_FOLDER']
        logger.debug(f"Upload directory: {upload_dir}")
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_dir, filename)
        logger.debug(f"Saving file to: {filepath}")
        
        # Save the file
        try:
            file.save(filepath)
            logger.debug("File saved successfully")
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return jsonify({'error': f'Error saving file: {str(e)}'}), 500
        
        # Extract text from the PDF
        try:
            logger.debug("Starting PDF text extraction")
            text = extract_text_from_pdf(filepath)
            logger.debug(f"Successfully extracted {len(text)} characters from PDF")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}\n{traceback.format_exc()}")
            # Clean up the file if text extraction fails
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug("Cleaned up failed upload file")
            return jsonify({'error': f'Error extracting text from PDF: {str(e)}'}), 400
        
        # Get the previous version if it exists
        try:
            logger.debug("Looking for previous version")
            previous_files = sorted([f for f in os.listdir(upload_dir) if f.endswith('.pdf')])
            logger.debug(f"Found {len(previous_files)} previous files")
            
            if len(previous_files) > 1:
                previous_file = previous_files[-2]  # Get the second-to-last file
                logger.debug(f"Using previous file: {previous_file}")
                previous_text = extract_text_from_pdf(os.path.join(upload_dir, previous_file))
                logger.debug("Starting difference analysis")
                differences = analyze_differences(previous_text, text)
                logger.debug("Difference analysis completed")
                logger.debug(differences)

            else:
                logger.debug("No previous version found, using default differences")
                differences = {
                    "content_changes": ["This is the first version of the pitch deck"],
                    "meaning_changes": [],
                    "additions": [],
                    "removals": [],
                    "tone_changes": []
                }
        except Exception as e:
            logger.error(f"Error analyzing differences: {str(e)}\n{traceback.format_exc()}")
            return jsonify({'error': f'Error analyzing differences: {str(e)}'}), 400
        
        logger.debug("Upload process completed successfully")
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'differences': differences
        })
        
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Upload error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred while processing the file'}), 500 