from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from ..utils.pdf_utils import extract_text_from_pdf
from ..utils.ai_utils import analyze_differences

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from the PDF
        text = extract_text_from_pdf(filepath)
        
        # Get the previous version if it exists
        previous_files = sorted([f for f in os.listdir(current_app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')])
        if len(previous_files) > 1:
            previous_file = previous_files[-2]  # Get the second-to-last file
            previous_text = extract_text_from_pdf(os.path.join(current_app.config['UPLOAD_FOLDER'], previous_file))
            differences = analyze_differences(previous_text, text)
        else:
            differences = {
                "content_changes": ["This is the first version of the pitch deck"],
                "meaning_changes": [],
                "additions": [],
                "removals": [],
                "tone_changes": []
            }
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'differences': differences
        })
    
    return jsonify({'error': 'Invalid file type'}), 400 