
from flask import Flask, request, jsonify, send_file
import tempfile
import os
import json
import zipfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from kpi_analysis import process_files  # Appelle ton script enrichi

app = Flask(__name__)

def generate_pdf(result, output_dir):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("report_template.html")
    try:
        html_out = template.render(data=result)
        pdf_path = os.path.join(output_dir, f"{result['chatteur']}.pdf")
        HTML(string=html_out).write_pdf(pdf_path)
    except Exception as e:
        print(f"[PDF ERROR] {result['chatteur']} → {e}")

@app.route('/parse', methods=['POST'])
def parse():
    if 'chatteurs' not in request.files or 'creator' not in request.files:
        return jsonify({'error': 'Les deux fichiers "chatteurs" et "creator" sont requis'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        chatteur_path = os.path.join(tmpdir, "chatteurs.xlsx")
        creator_path = os.path.join(tmpdir, "creator.xlsx")
        request.files['chatteurs'].save(chatteur_path)
        request.files['creator'].save(creator_path)

        # 📥 Génération des JSON enrichis
        results = process_files(chatteur_path, creator_path, tmpdir)

        # 📄 Génération PDF à partir du JSON
        for result in results:
            generate_pdf(result, tmpdir)

        # 📦 Création de l’archive de sortie
        zip_path = os.path.join(tmpdir, "outputs.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for result in results:
                name = result["chatteur"]
                zipf.write(os.path.join(tmpdir, f"Rapport_{name}.json"), arcname=f"Rapport_{name}.json")
                zipf.write(os.path.join(tmpdir, f"{name}.pdf"), arcname=f"{name}.pdf")

        return send_file(zip_path, as_attachment=True, download_name="outputs.zip")
