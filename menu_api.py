import os
import json
from pathlib import Path
from flask import Flask, request, jsonify

from pdf_to_text import extract_text_hybrid
from query_llm import query_model_to_json

app = Flask(__name__)

# Define the directory to save uploaded PDFs (you can change this)
UPLOAD_FOLDER = './example_pdfs'
OUTPUT_FOLDER = './output_jsons'

# Ensure the upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Set the upload folder for Flask to save the files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to process an uploaded PDF and return JSON
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file part"}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        # Save the file to the uploads directory
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        filename = Path(file.filename)

        try:
            # Extract text from the PDF and query the LLM for JSON
            extracted_text = extract_text_hybrid(file_path)
            menu_json = query_model_to_json(extracted_text)
            
            # Save the generated JSON to the output folder
            json_filename = filename.with_suffix(".json")
            json_path = os.path.join(OUTPUT_FOLDER, json_filename)
            with open(json_path, 'w') as json_file:
                json.dump(menu_json, json_file, indent=2)

            return jsonify(menu_json), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400

# Route to process a PDF from the server's file system and return JSON
@app.route('/process-pdf', methods=['GET'])
def process_pdf():
    pdf_filename = request.args.get('pdf')
    if not pdf_filename:
        return jsonify({"error": "No PDF filename provided"}), 400
    filename = Path(pdf_filename)

    file_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    if not os.path.exists(file_path):
        return jsonify({"error": f"File {pdf_filename} not found"}), 404

    try:
        # Extract text from the PDF and query the LLM for JSON
        extracted_text = extract_text_hybrid(file_path)
        menu_json = query_model_to_json(extracted_text)

        # Save the generated JSON to the output folder
        json_filename = filename.with_suffix(".json")
        json_path = os.path.join(OUTPUT_FOLDER, json_filename)
        with open(json_path, 'w') as json_file:
            json.dump(menu_json, json_file, indent=2)

        return jsonify(menu_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
