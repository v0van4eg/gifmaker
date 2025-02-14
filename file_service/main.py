# file_service/main.py
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
uploads_root = os.path.join(app.root_path, 'uploads')

# Фильтр допустимых форматов
def allowed_file(filename):
    return filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'))

@app.route('/upload', methods=['POST'])
def upload():
    session_id = request.form.get('session_id')
    logger.info(f"Received session ID in file_service: {session_id}")
    if not session_id:
        return jsonify(error='Session ID not found'), 400
    upload_folder = os.path.join(uploads_root, session_id)
    os.makedirs(upload_folder, exist_ok=True)
    files = request.files.getlist('files')
    if not files:
        return jsonify(error='No selected files'), 400
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            try:
                file.save(file_path)
                logger.info(f"Saved file {filename} to {file_path}")
            except Exception as e:
                return jsonify(error=f'Failed to save file: {str(e)}'), 500
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)