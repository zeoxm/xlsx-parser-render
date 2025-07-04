import pandas as pd
import os
import json
import zipfile
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

def generate_pdf(result, output_dir):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("report_template.html")
    try:
        html_out = template.render(data=result)
        pdf_path = os.path.join(output_dir, f"{result['chatteur']}.pdf")
        HTML(string=html_out).write_pdf(pdf_path)
    except Exception as e:
        print(f"[PDF ERROR] {result['chatteur']} → {e}")

def process_files(chatteurs_file, creator_file, temp_dir):
    df_chat = pd.read_excel(chatteurs_file)
    df_creator = pd.read_excel(creator_file)
    semaine = pd.to_datetime("today").strftime("%Y-%m-%d")
    json_data_list = []

    for _, row in df_chat.iterrows():
        chatteur = row["Employees"]
        modele = row["Group"]
        creator_row = df_creator[df_creator["Group"] == modele]
        ca_total = creator_row["Total earnings Net ($)"].values[0] if not creator_row.empty else 0.0
        fans_total = int(creator_row["Active fans"].values[0]) if not creator_row.empty else 0

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
            "$/h net": round(result["salaire_net"] / (row["Clocked minutes"] / 60), 2) if row["Clocked minutes"] > 0 else None,
            "note": "Faire clock in le chatteur" if row["Clocked minutes"] == 0 else "",
            "chatteur": chatteur,
            "modele": modele,
            "semaine": semaine,
            "SPC": spc,
            "dollars_per_hour": round(float(row.get("CA / min", 0)) * 60, 2),
            "flags": ", ".join(map(str, flags)) if flags else "—",
            "typologies": ", ".join(map(str, typologies[:2])) if typologies else "—",
            "axe": axe if axe else "—",
            "modules": ", ".join(map(str, modules)) if modules else "—",
            "appel": appel if appel else "Non",
            "salaire_net": round(float(row.get("Sales", 0)) * 0.15 + 0.0, 2),
            "ajustement": 0.0,
            "ca_modele": ca_total,
            "fans_modele": fans_total
        }

        # Sauvegarde JSON
        json_path = os.path.join(temp_dir, f"{chatteur}.json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Génère PDF
        generate_pdf(result, temp_dir)

        # Ajoute à la liste
        json_data_list.append(result)

    # Génère Synthese_Manager.xlsx
    synthese_path = os.path.join(temp_dir, "Synthese_Manager.xlsx")
    generate_synthese_manager(json_data_list, synthese_path)

    # Crée archive .zip
    zip_path = os.path.join(temp_dir, "outputs.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for result in json_data_list:
            name = result["chatteur"]
            zipf.write(os.path.join(temp_dir, f"{name}.json"), arcname=f"{name}.json")
            zipf.write(os.path.join(temp_dir, f"{name}.pdf"), arcname=f"{name}.pdf")
        zipf.write(synthese_path, arcname="Synthese_Manager.xlsx")

    return zip_path
