
import pandas as pd
import os
import re
import traceback
import json
from datetime import datetime
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

def process_files(chatteurs_file, creator_file, temp_dir):
    df_chat = pd.read_excel(chatteurs_file)
    df_creator = pd.read_excel(creator_file)

    #KPIs
    df_chat['Golden ratio'] = df_chat['Golden ratio'].apply(convert_percent)
    df_chat['Unlock ratio'] = df_chat['Unlock ratio'].apply(convert_percent)
    df_chat['Scheduled minutes'] = df_chat['Scheduled hours'].apply(convert_time_to_minutes)
    df_chat['Clocked minutes'] = df_chat['Clocked hours'].apply(convert_time_to_minutes)
    df_chat['Inactivité'] = df_chat['Scheduled minutes'] - 40 - df_chat['Clocked minutes']
    df_chat['Prix moyen'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['PPVs unlocked']), axis=1)
    df_chat['CA / fan'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['Fans chatted']), axis=1)
    df_chat['Messages / fan'] = df_chat.apply(lambda row: safe_divide(row['Messages sent'], row['Fans chatted']), axis=1)
    df_chat['Keystrokes / msg'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Messages sent']), axis=1)
    df_chat['Keystrokes / fan'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Fans chatted']), axis=1)
    df_chat['CA / min'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['Clocked minutes']), axis=1)
    df_chat['Messages / min'] = df_chat.apply(lambda row: safe_divide(row['Messages sent'], row['Clocked minutes']), axis=1)
    df_chat['Keystrokes / min'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Clocked minutes']), axis=1)
    df_chat['Salaire brut'] = df_chat['Sales'] * 0.15
    df_chat['Salaire net'] = df_chat['Salaire brut']
    df_chat['Ajustement'] = 0

    semaine = datetime.today().date() - pd.to_timedelta(datetime.today().weekday(), unit='D')
    semaine = semaine.strftime("%Y-%m-%d")

    results = []
    output_paths = []
    
    for index, row in df_chat.iterrows():
        chatteur = row['Employees']
        modele = row['Group']
        print(f"--- Traitement du chatteur : {chatteur}")
        safe_chatteur = re.sub(r'[^a-zA-Z0-9_-]', '_', chatteur)
        safe_modele = re.sub(r'[^a-zA-Z0-9_-]', '_', modele)
        chatteur = row ['Employees']
        modele = row['Group']

        creator_row = df_creator[df_creator['Creator'] == modele]
        if not creator_row.empty:
            raw_value = str(creator_row['Total earnings Net'].values[0]).replace(',', '.').replace('$', '')
        result = None
        try:
                ca_total = float(re.findall(r"[\d.]+", raw_value)[0])
        except:
                ca_total = 0.0
                fans_total = int(creator_row['Active fans'].values[0])
        else:
            ca_total = 0.0
            fans_total = 0

        context = {
            "CA_model": ca_total,
            "fans_model": fans_total,
            "chatteurs_model": len(df_chat)
        }

        flags = detect_flags(row, context)
        typologies = detect_typologies(row, context)
        spc, spc_details = compute_spc(row, typologies)
        axe, modules, appel = compute_coaching_axis(row, flags, typologies, spc, context)

        result = None

        try:
            result = {
                "chatteur": chatteur,
                "modele": modele,
                "semaine": semaine,
                "SPC": spc,
                "$/h": round(float(row.get('CA / min', 0)) * 60, 2),
                "flags": ", ".join(map(str, flags)) if flags else "-",
                "typologies": ", ".join(map(str, typologies[:2])) if typologies else "-",
                "axe": axe if axe else "-",
                "modules": ", ".join(map(str, modules)) if modules else "-",
                "appel_managérial": appel,
                "salaire_brut": round(row['Salaire brut'], 2),
                "ajustement": 0,
                "salaire_net": round(row['Salaire net'], 2),
                "CA_model": round(ca_total, 2),
                "fans_model": int(fans_total),
            }

            for col in df_chat.columns:
                result[col] = row[col] if not pd.isna(row[col]) else None

        # Export PDF
                template_dir = os.path.dirname(os.path.abspath(__file__))
                env = Environment(loader=FileSystemLoader(template_dir))
                template = env.get_template("report_template.html")
                html_out = template.render(data=result)
                pdf_path = os.path.join(temp_dir, f"{safe_chatteur}_{semaine}.pdf")
                HTML(string=html_out).write_pdf(pdf_path)
                output_paths.append(pdf_path)

        # Export JSON
                json_path = os.path.join(temp_dir, f"{safe_chatteur}_{semaine}.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                    output_paths.append(json_path)

        except Exception as e:
             print(f"Erreur sur {chatteur} : {e}")
             traceback.print_exc()
              print(f"Erreur sur {chatteur} : {e}")
              traceback.print_exc()

        if result:
            results.append(result)

        return results, semaine, output_paths
