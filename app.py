import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from docx import Document
from PyPDF2 import PdfReader

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files[]' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    files = request.files.getlist('files[]')
    language = request.form.get('language', 'eng')

    final_text = ""

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.lower().endswith('.pdf'):
            pdf = PdfReader(filepath)
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    final_text += text + "\n"
        else:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img, lang=language)
            final_text += text + "\n"

    return jsonify({'status': 'success', 'text': final_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
