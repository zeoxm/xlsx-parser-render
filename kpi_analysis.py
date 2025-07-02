from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
import os
import re
from datetime import datetime
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

    fans_total = df_creator['Active fans'].sum()
    nb_chatteurs = len(df_chat)
    semaine = datetime.today().date() - pd.to_timedelta(datetime.today().weekday(), unit='D')
    semaine = semaine.strftime("%Y-%m-%d")

    results = []

    for index, row in df_chat.iterrows():
        chatteur = row['Employees']
        modele = row['Group']

        creator_row = df_creator[df_creator['Creator'] == modele]

        if not creator_row.empty:
            raw_value = str(creator_row['Total earnings Net'].values[0]).replace(',', '.').replace('$', '')
            try:
                ca_total = float(re.findall(r"[\d.]+", raw_value)[0])
            except:
                ca_total = 0.0
        else:
            ca_total = 0.0

        context = {
            "CA_model": ca_total,
            "fans_model": fans_total,
            "chatteurs_model": nb_chatteurs
        }

        flags = detect_flags(row, context)
        typologies = detect_typologies(row, context)
        spc, spc_details = compute_spc(row, typologies)
        axe, modules, appel = compute_coaching_axis(row, flags, typologies, spc, context)

        result = {
            "chatteur": chatteur,
            "modele": modele,
            "semaine": semaine,
            "SPC": spc,
            "$/h": round(row['CA / min'] * 60, 2),
            "flags": flags,
            "typologies": typologies[:2],
            "axe": axe,
            "modules": modules,
            "appel_managérial": appel,
            "salaire_brut": round(row['Salaire brut'], 2),
            "ajustement": 0,
            "salaire_net": round(row['Salaire net'], 2),
            "CA_model": round(ca_total, 2),
            "fans_model": int(fans_total),
        }

        for col in df_chat.columns:
            result[col] = row[col] if not pd.isna(row[col]) else None

        
        # Génération du PDF lisible
        pdf_path = os.path.join(temp_dir, f"{chatteur}_{semaine}.pdf")
        try:
            generate_pdf(result, pdf_path)
        except Exception as e:
            print(f"Erreur PDF {chatteur}: {e}")
        results.append(result)
    
        def generate_pdf(data, output_path):
        try:
            env = Environment(loader=FileSystemLoader("."))
            template = env.get_template("report_template.html")

            html_out = template.render(data=entry)
                chatteur=data["chatteur"],
                modele=data["modele"],
                semaine=data["semaine"],
                SPC=data["SPC"],
                dollar_per_hour=data["$/h"],
                axe=data["axe"],
                modules=", ".join(data["modules"]),
                appel="Oui" if data["appel_managérial"] else "Non",
                flags=", ".join(data["flags"]),
                typologies=", ".join(data["typologies"]),
                CA=f'{round(data["Sales"], 2)} $',
                prix_moyen=f'{round(data["Prix moyen"], 2)} $',
                ppv=int(data["PPVs unlocked"]),
                push=int(data["PPVs sent"]),
                fans=int(data["Fans chatted"]),
                golden_ratio=round(data["Golden ratio"], 2)
                )

            HTML(string=html_out).write_pdf(output_path)
         except Exception as e:
            print(f"Erreur PDF : {e}")
