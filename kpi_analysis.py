
import pandas as pd
import numpy as np
import json
import os

def convert_percent(value):
    try:
        return float(str(value).replace('%', '').strip())
    except:
        return 0.0

def safe_divide(a, b):
    return round(a / b, 2) if b else 0.0

def process_files(chatteurs_path, creator_path, output_dir):
    df_chat = pd.read_excel(chatteurs_path)
    df_creator = pd.read_excel(creator_path)

    df_chat['Golden ratio'] = df_chat['Golden ratio'].apply(convert_percent)
    df_chat['Unlock ratio'] = df_chat['Unlock ratio'].apply(convert_percent)

    results = []

    for index, row in df_chat.iterrows():
        employee = row.get("Employees", "-")
        group = row.get("Group", "-")
        sales = row.get("Sales", 0.0)
        ppvs_unlocked = row.get("PPVs unlocked", 0)
        ppvs_sent = row.get("PPVs sent", 0)
        fans_chatted = row.get("Fans chatted", 0)
        messages_sent = row.get("Messages sent", 0)
        keystrokes = row.get("Keystrokes (words)", 0)
        clocked_minutes = row.get("Clocked minutes", 0)
        scheduled_minutes = row.get("Scheduled minutes", 0)

        result = {
            "chatteur": employee,
            "modele": group,
            "semaine": "2025-06-23",
            "Sales": sales,
            "PPVs envoyés": ppvs_sent,
            "PPVs débloqués": ppvs_unlocked,
            "Unlock ratio": row["Unlock ratio"],
            "Golden ratio": row["Golden ratio"],
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
            "Inactivité": scheduled_minutes - 40 - clocked_minutes,
            "Clocked minutes": clocked_minutes,
            "Scheduled minutes": scheduled_minutes,
            "$/h net": safe_divide(sales, (clocked_minutes - 40) / 60) if clocked_minutes > 40 else 0,
            "salaire_net": round(sales * 0.15, 2)
        }

        file_name = f"{employee}.json"
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        results.append(result)

    return results
