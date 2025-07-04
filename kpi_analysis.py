
import pandas as pd
import numpy as np

def process_files(chatteurs_path, creator_path, output_dir):
    df_chat = pd.read_excel(chatteurs_path)
    df_creator = pd.read_excel(creator_path)

    for index, row in df_chat.iterrows():
        creator_row = df_creator[df_creator['Creator'] == row['Employees']].squeeze()

        salaire_brut = row["Sales"] * 0.15
        salaire_net = round(salaire_brut, 2)
        try:
            sales = round(salaire_net / 0.15, 2)
        except ZeroDivisionError:
            sales = 0

        result = {
            "chatteur": row["Employees"],
            "modele": row["Group"],
            "semaine": "2025-06-23",
            "SPC": 85,
            "axe": "Optimiser les conversions",
            "typologies": "Low clock",
            "flags": "Inactif",
            "modules": "2, 3",
            "appel": "Non",
            "note": "Néant",
            "salaire_net": salaire_net,
            "$/h net": 25,
            "Clocked minutes": row.get("Clocked hours", 0) * 60 if isinstance(row.get("Clocked hours"), (int, float)) else 0,
            "Prix moyen": row.get("Sales", 0) / row.get("PPVs unlocked", 1),
            "CA / fan": row.get("Sales", 0) / row.get("Fans chatted", 1),
            "Keystrokes / msg": row.get("Keystrokes (words)", 0) / row.get("Messages sent", 1),
            "CA / min": row.get("Sales", 0) / (row.get("Clocked hours", 0) * 60 + 1),
            "Inactivité": "Non",
            "Reply time": row.get("Reply time"),
            "sales": sales,
            "new_subs": creator_row.get("New subscriptions Net") if not creator_row.empty else None,
            "tips_net": creator_row.get("Tips Net") if not creator_row.empty else None,
            "messages_net": creator_row.get("Message Net") if not creator_row.empty else None,
            "earnings_net": creator_row.get("Total earnings Net") if not creator_row.empty else None,
            "ca_modele": creator_row.get("Total earnings Net") if not creator_row.empty else None,
            "fans_modele": creator_row.get("Active fans") if not creator_row.empty else None
        
        "Fans chatted": row.get("Fans chatted"),
        "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2),

    }

        # Simuler l'enregistrement JSON
        print(f"Génération JSON pour {result['chatteur']}: OK")
