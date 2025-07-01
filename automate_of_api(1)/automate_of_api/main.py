from flask import Flask, request, jsonify, send_file
import tempfile
import os
import zipfile
import shutil
from kpi_analysis import process_files
from generate_xlsx import generate_synthese_manager

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    if 'chatteurs' not in request.files or 'creator' not in request.files:
        return jsonify({'error': 'Les deux fichiers "chatteurs" et "creator" sont requis'}), 400

    chatteurs_file = request.files['chatteurs']
    creator_file = request.files['creator']

    with tempfile.TemporaryDirectory() as temp_dir:
        json_data_list, semaine = process_files(chatteurs_file, creator_file, temp_dir)
        xlsx_path = os.path.join(temp_dir, "Synthese_Manager.xlsx")
        generate_synthese_manager(json_data_list, xlsx_path)
        zip_path = os.path.join(temp_dir, "outputs.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for json_data in json_data_list:
                filename = f"{json_data['chatteur']}.json"
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    import json
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                zipf.write(filepath, arcname=filename)
            zipf.write(xlsx_path, arcname="Synthese_Manager.xlsx")

        return send_file(zip_path, mimetype='application/zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
