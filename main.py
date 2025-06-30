
from flask import Flask, request, jsonify
import json
from utils.parsers import parse_exports
from utils.generators import generate_docx, generate_pdf, generate_xlsx, update_json_with_adjustments, finalize_reports

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    inflow_file = request.files.get('inflow')
    creator_file = request.files.get('creator')
    if not inflow_file or not creator_file:
        return jsonify({'error': 'Missing files'}), 400
    result = parse_exports(inflow_file, creator_file)
    return jsonify(result)

@app.route('/generate-docx', methods=['POST'])
def generate_docx_route():
    data = request.get_json()
    return generate_docx(data)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf_route():
    data = request.get_json()
    return generate_pdf(data)

@app.route('/generate-xlsx', methods=['POST'])
def generate_xlsx_route():
    data = request.get_json()
    return generate_xlsx(data)

@app.route('/update-json-with-adjustments', methods=['POST'])
def update_json():
    json_data = request.get_json()
    return update_json_with_adjustments(json_data)

@app.route('/finalize-reports', methods=['POST'])
def finalize():
    data = request.get_json()
    return finalize_reports(data)

if __name__ == '__main__':
    app.run()
