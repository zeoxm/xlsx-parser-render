
from flask import Flask, request, jsonify, send_file
import tempfile
import os
import json
import zipfile
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from kpi_analysis import process_files
from generate_xlsx import generate_synthese_manager

app = Flask(__name__)

def generate_pdf(result, output_dir):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("report_template.html")
    try:
        html_out = template.render(data=result)
        pdf_name = f"{result['chatteur']}.pdf"
        pdf_path = os.path.join(output_dir, pdf_name)
        HTML(string=html_out).write_pdf(pdf_path)
        print(f"[✅ PDF] {pdf_name}")
    except Exception as e:
        print(f"[PDF ERROR] {result.get('chatteur', 'inconnu')} → {e}")

@app.route('/parse', methods=['POST'])
def parse():
    if 'chatteurs' not in request.files or 'creator' not in request.files:
        return jsonify({'error': 'Les deux fichiers "chatteurs" et "creator" sont requis'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        chatteur_path = os.path.join(tmpdir, "chatteurs.xlsx")
        creator_path = os.path.join(tmpdir, "creator.xlsx")
        request.files['chatteurs'].save(chatteur_path)
        request.files['creator'].save(creator_path)

        print("[📊 Analyse] Lecture des fichiers .xlsx...")
        results = process_files(chatteur_path, creator_path, tmpdir)

        # Générer PDF et logger
        for result in results:
            json_name = f"Rapport_{result['chatteur']}.json"
            json_path = os.path.join(tmpdir, json_name)
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(result, jf, indent=4, ensure_ascii=False)
            json_path = os.path.join(tmpdir, json_name)
            if os.path.exists(json_path):
                print(f"[✅ JSON] {json_name}")
            else:
                print(f"[❌ JSON MANQUANT] {json_name}")
            generate_pdf(result, tmpdir)

        xlsx_path = os.path.join(tmpdir, "Synthese_Manager.xlsx")
        generate_synthese_manager(results, xlsx_path)
        print("[✅ XLSX] Synthese_Manager.xlsx généré")

        # Créer le ZIP final
        zip_path = os.path.join(tmpdir, "outputs.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for result in results:
                name = result["chatteur"]
                json_file = os.path.join(tmpdir, f"Rapport_{name}.json")
                pdf_file = os.path.join(tmpdir, f"{name}.pdf")
                if os.path.exists(json_file):
                    zipf.write(json_file, arcname=f"Rapport_{name}.json")
                if os.path.exists(pdf_file):
                    zipf.write(pdf_file, arcname=f"{name}.pdf")
            zipf.write(xlsx_path, arcname="Synthese_Manager.xlsx")

        print("[📦 ZIP] outputs.zip prêt")
        return send_file(zip_path, as_attachment=True, download_name="outputs.zip")