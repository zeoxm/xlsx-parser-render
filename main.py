from flask import Flask, request, jsonify, send_file
import tempfile
import os
import json
import zipfile
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from utils import (
    convert_time_to_minutes,
    convert_percent,
    safe_divide,
    detect_flags,
    detect_typologies,
    compute_spc,
    compute_coaching_axis
)
from generate_xlsx import generate_synthese_manager

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

    chatteurs_file = request.files['chatteurs']
    creator_file = request.files['creator']

    with tempfile.TemporaryDirectory() as temp_dir:
        df_chat = pd.read_excel(chatteurs_file)
        df_creator = pd.read_excel(creator_file)

        print("✅ Colonnes fichier chatteurs :", df_chat.columns.tolist())
        print("✅ Colonnes fichier creator :", df_creator.columns.tolist())

        df_chat["Unlock ratio"] = df_chat["Unlock ratio"].apply(convert_percent)
        df_chat["Golden ratio"] = df_chat["Golden ratio"].apply(convert_percent)

        semaine = pd.to_datetime("today").strftime("%Y-%m-%d")
        json_data_list = []

        for _, row in df_chat.iterrows():
            try:
                chatteur = row["Employees"]
                modele = row["Group"]
            except KeyError as e:
                raise ValueError(f"[ERREUR CRITIQUE] Colonne manquante dans le fichier chatteurs : {e}")

            try:
                creator_row = df_creator[df_creator["Group"] == modele]
            except KeyError:
                creator_row = df_creator[df_creator["Creator"] == modele]

            if not creator_row.empty:
                try:
                    raw = str(creator_row["Total earnings Net"].values[0]).replace(",", ".").replace("$", "")
                    ca_total = float(raw)
                except:
                    ca_total = 0.0
                try:
                    fans_total = int(creator_row["Active fans"].values[0])
                except:
                    fans_total = 0
            else:
                ca_total = 0.0
                fans_total = 0

            # 🔁 KPIs calculés manuellement injectés dans row
            try:
                row["Prix moyen"] = float(row["Sales"]) / float(row["PPVs unlocked"]) if row["PPVs unlocked"] > 0 else 0
            except:
                row["Prix moyen"] = 0
            try:
                row["CA / fan"] = float(row["Sales"]) / float(row["Fans chatted"]) if row["Fans chatted"] > 0 else 0
            except:
                row["CA / fan"] = 0
            try:
                row["Keystrokes / msg"] = float(row["Keystrokes (words)"]) / float(row["Messages sent"]) if row["Messages sent"] > 0 else 0
            except:
                row["Keystrokes / msg"] = 0
            try:
                row["Clocked minutes"] = float(row["Clocked hours"]) * 60
            except:
                row["Clocked minutes"] = 0
            try:
                row["Scheduled minutes"] = float(row["Scheduled hours"]) * 60
            except:
                row["Scheduled minutes"] = 0
            try:
                row["CA / min"] = float(row["Sales"]) / row["Clocked minutes"] if row["Clocked minutes"] > 0 else 0
            except:
                row["CA / min"] = 0
            try:
                row["Inactivité"] = float(row["Reply time"])
            except:
                row["Inactivité"] = 0

            context = {
                "CA_model": ca_total,
                "fans_model": fans_total,
                "chatteurs_model": len(df_chat)
            }

            flags = detect_flags(row, context)
            typologies = detect_typologies(row, context)
            spc, _ = compute_spc(row, typologies)
            axe, modules, appel = compute_coaching_axis(row, flags, typologies, spc, context)

            result = {
            "Prix moyen": float(row.get("Prix moyen", 0)),
            "CA / fan": float(row.get("CA / fan", 0)),
            "Keystrokes / msg": float(row.get("Keystrokes / msg", 0)),
            "Clocked minutes": float(row.get("Clocked minutes", 0)),
            "Scheduled minutes": float(row.get("Scheduled minutes", 0)),
            "CA / min": float(row.get("CA / min", 0)),
            "Inactivité": float(row.get("Inactivité", 0)),
                "ca_modele": ca_total,
                "fans_modele": fans_total,
                                "ajustement": 0.0,
                "salaire_net": round(float(row.get("Sales", 0)) * 0.15 + 0.0, 2),
                "dollars_per_hour": round(row["CA / min"] * 60, 2),
                "chatteur": chatteur,
                "modele": modele,
                "semaine": semaine,
                "SPC": spc,
                "dollars_per_hour": round(row["CA / min"] * 60, 2),
                "flags": ", ".join(map(str, flags)) if flags else "—",
                "typologies": ", ".join(map(str, typologies[:2])) if typologies else "—",
                "axe": axe if axe else "—",
                "modules": ", ".join(map(str, modules)) if modules else "—",
                "appel": appel if appel else "Non",
                "salaire": round(float(row.get("Sales", 0)) * 0.15, 2)
            }

            json_path = os.path.join(temp_dir, f"{chatteur}.json")
            with open(json_path, "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            generate_pdf(result, temp_dir)
            json_data_list.append(result)

        synthese_path = os.path.join(temp_dir, "Synthese_Manager.xlsx")
        generate_synthese_manager(json_data_list, synthese_path)

        zip_path = os.path.join(temp_dir, "outputs.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for result in json_data_list:
                name = result["chatteur"]
                zipf.write(os.path.join(temp_dir, f"{name}.json"), arcname=f"{name}.json")
                zipf.write(os.path.join(temp_dir, f"{name}.pdf"), arcname=f"{name}.pdf")
            zipf.write(synthese_path, arcname="Synthese_Manager.xlsx")

        return send_file(zip_path, as_attachment=True, download_name="outputs.zip")
