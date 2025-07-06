
import pandas as pd
import numpy as np
import json
import os
import re

def convert_percent(value):
    try:
        return float(str(value).replace('%', '').strip())
    except:
        return 0.0

def safe_divide(a, b):
    return round(a / b, 2) if b else 0.0

def convert_to_minutes(time_str):
    if pd.isna(time_str):
        return 0
    time_str = str(time_str).lower().replace(' ', '')
    h = re.search(r"(\d+)h", time_str)
    m = re.search(r"(\d+)(mn|min|m)", time_str)
    hours = int(h.group(1)) if h else 0
    minutes = int(m.group(1)) if m else 0
    return hours * 60 + minutes

def clean_columns(df):
    df.columns = [str(col).strip() for col in df.columns]
    return df

def process_files(chatteurs_path, creator_path, output_dir):
    df_chat = pd.read_excel(chatteurs_path)
    df_creator = pd.read_excel(creator_path)

    df_chat = clean_columns(df_chat)
    df_creator = clean_columns(df_creator)

    if "Group" not in df_chat.columns or "Employees" not in df_chat.columns:
        raise KeyError("Colonne 'Group' ou 'Employees' manquante dans le fichier Chatteurs.")

    df_chat['Golden ratio'] = df_chat['Golden ratio'].apply(convert_percent)
    df_chat['Unlock ratio'] = df_chat['Unlock ratio'].apply(convert_percent)
    df_chat['Clocked minutes'] = df_chat['Clocked hours'].apply(convert_to_minutes)
    df_chat['Scheduled minutes'] = df_chat['Scheduled hours'].apply(convert_to_minutes)
    df_chat['Inactivité'] = df_chat['Scheduled minutes'] - 40 - df_chat['Clocked minutes']

    results = []

    for index, row in df_chat.iterrows():
        employee = str(row.get("Employees", f"inconnu_{index}")).strip()
        group = str(row.get("Group", "-")).strip()

        creator_row = df_creator[df_creator["Creator group"] == group]
        if not creator_row.empty:
            try:
                ca_modele = float(str(creator_row["Total earnings Net"].values[0]).replace("$", "").replace(",", "."))
            except:
                ca_modele = 0.0
            try:
                fans_modele = int(creator_row["Active fans"].values[0])
            except:
                fans_modele = 0
            try:
                subs_modele = int(creator_row["New fans"].values[0])
            except:
                subs_modele = 0
        else:
            ca_modele = 0.0
            fans_modele = 0
            subs_modele = 0

        sales = row.get("Sales", 0.0)
        ppvs_unlocked = row.get("PPVs unlocked", 0)
        fans_chatted = row.get("Fans chatted", 0)
        messages_sent = row.get("Messages sent", 0)
        keystrokes = row.get("Keystrokes (words)", 0)
        clocked_minutes = row.get("Clocked minutes", 0)

        result = {
            "chatteur": employee,
            "modele": group,
            "semaine": "2025-06-23",
            "Sales": sales,
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": ppvs_unlocked,
            "Unlock ratio": row.get("Unlock ratio", 0),
            "Golden ratio": row.get("Golden ratio", 0),
            "Messages envoyés": messages_sent,
            "Fans chatted": fans_chatted,
            "Messages / fan": safe_divide(messages_sent, fans_chatted),
            "Reply time": row.get("Reply time", "—"),
            "Prix moyen": safe_divide(sales, ppvs_unlocked),
            "CA / fan": safe_divide(sales, fans_chatted),
            "CA / min": safe_divide(sales, clocked_minutes),
            "Keystrokes / msg": safe_divide(keystrokes, messages_sent),
            "Keystrokes / fan": safe_divide(keystrokes, fans_chatted),
            "Messages / min": safe_divide(messages_sent, clocked_minutes),
            "Inactivité": row.get("Inactivité", 0),
            "Clocked minutes": clocked_minutes,
            "Scheduled minutes": row.get("Scheduled minutes", 0),
            "$/h net": safe_divide(sales, (clocked_minutes - 40) / 60) if clocked_minutes > 40 else 0,
            "salaire_net": round(sales * 0.15, 2),
            "ca_modele": ca_modele,
            "fans_modele": fans_modele,
            "subs_modele": subs_modele,
            "ca_par_sub": safe_divide(ca_modele, subs_modele),
            "ratio_clocksched": safe_divide(clocked_minutes, row.get("Scheduled minutes", 1)) * 100
        }

        file_name = f"Rapport_{employee}.json"
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        results.append(result)

    return results
