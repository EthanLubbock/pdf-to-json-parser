# Drinks Menu PDF Processor

The **Drinks Menu PDF Processor** is designed to extract structured information from drinks menus stored in PDF format. The project includes two primary components:
1. **Jupyter Notebook**: A notebook that processes PDF files, extracts text, queries an LLM to generate structured JSON data, and saves it in a target directory.
2. **Flask API**: A lightweight API to process PDFs, either via file upload or by providing a file path, and return the corresponding JSON output.

The aim of this project is to facilitate easy extraction of product details (such as names, descriptions, prices, and brands) from drinks menus in PDF format and present this data in a structured, machine-readable format.

## Installation Instructions
1. Setup virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Install tesseract-ocr (https://tesseract-ocr.github.io/tessdoc/Installation.html)
   ```bash
   sudo apt install tesseract-ocr
4. Setup Gemini API key environment variable (https://aistudio.google.com/apikey)
   ```bash
   export GEMINI_API_KEY="your-gemini-key"
## Jupyter Notebook: `process_drinks_menu.ipynb`
The Jupyter Notebook is designed to process drinks menu PDFs. The workflow is as follows:
##### How to Use:
1. Place the PDF files you wish to process in the `./example_pdfs` directory.
2. Open the Jupyter Notebook `process_drinks_menus.ipynb` and execute the cells step by step.
3. The generated JSON files will be saved in the `./output_jsons` directory.

## Flask API: `menu_api.py`
The Flask API provides two main endpoints:

- `/upload-pdf`: Accepts a PDF file upload and returns the corresponding JSON data.
- `/process-pdf`: Accepts a file path of a previously uploaded PDF and returns the generated JSON data.

Run the following command to start the Flask API:

```bash
python menu_api.py
```

##### Endpoints:
1. ```POST /upload-pdf```: Upload a PDF file and receive the JSON response.
   ```bash
   curl -X POST -F "pdf=@[path_to_your_pdf].pdf" http://127.0.0.1:5000/upload-pdf
    ```
2. ```GET /process-pdf```: Provide the filename of an uploaded PDF receive a JSON response.
    ```bash
    curl "http://127.0.0.1:5000/process-pdf?pdf=[pdf_filename].pdf"
    ```

## Next Steps and Enhancements
- **Evaluate**: The obvious next step is to assess the model's performance providing more data and seeing if it is able to match known groundtruth results.
- **Deployment**: Consider deploying the Flask API to a server or cloud platform like AWS Lambda for public use.
- **Enhanced OCR**: I feel the OCR is not going to be robust and there may be more edge cases to handle much like the existing dollar sign correction for ```bacardi_menu.pdf```