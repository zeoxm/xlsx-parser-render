
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
            result = {
            "chatteur": row.get("Employees", "-"),
            "modele": row.get("Group", "-"),
            "semaine": "2025-06-23",
            "SPC": 85,
            "axe": "Optimiser les conversions",
            "typologies": "Low clock",
            "flags": "Inactif",
            "modules": "2, 3",
            "appel": "Non",
            "note": "Néant",
            "salaire_net": round(row.get("Sales", 0.0) * 0.15, 2),
            "$/h net": 25,
            "Clocked minutes": row.get("Clocked minutes", 0),
            "Scheduled minutes": row.get("Scheduled minutes", 0),
            "Inactivité": row.get("Inactivité", 0),
            "Sales": row.get("Sales", 0.0),
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": row.get("PPVs unlocked", 0),
            "Unlock ratio": convert_percent(row.get("Unlock ratio", "0%")),
            "Golden ratio": convert_percent(row.get("Golden ratio", "0%")),
            "Messages envoyés": row.get("Messages sent", 0),
            "Fans chatted": row.get("Fans chatted", 0),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Reply time": row.get("Reply time", "—"),
            "Tips nets": row.get("Tips Net", 0.0),
            "Messages nets": row.get("Message Net", 0.0),
            "Total earnings": row.get("Total Earnings", 0.0),
            "Nouveaux subs": row.get("New Fans", 0),
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "CA / min": round(row.get("Sales", 0.0) / row.get("Clocked minutes", 1), 4) if row.get("Clocked minutes", 0) > 0 else 0,
            "Keystrokes / msg": round(row.get("Keystrokes (words)", 0) / row.get("Messages sent", 1), 2) if row.get("Messages sent", 0) > 0 else 0,
        }
            sales = 0

            "chatteur": row.get("Employees", "-"),
            "modele": row.get("Group", "-"),
            "semaine": "2025-06-23"

            "Sales": row.get("Sales", 0.0),
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": row.get("PPVs unlocked", 0),
            "Unlock ratio": convert_percent(row.get("Unlock ratio", "0%")),
            "Golden ratio": convert_percent(row.get("Golden ratio", "0%")),
            "Messages envoyés": row.get("Messages sent", 0),
            "Fans chatted": row.get("Fans chatted", 0),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Reply time": row.get("Reply time", "—"),
            "Tips nets": row.get("Tips Net", 0.0),
            "Messages nets": row.get("Message Net", 0.0),
            "Total earnings": row.get("Total Earnings", 0.0),
            "Nouveaux subs": row.get("New Fans", 0),
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "chatteur": row.get("Employees", "-"),
            "modele": row.get("Group", "-"),
            "semaine": "2025-06-23",
            "SPC": 85,
            "axe": "Optimiser les conversions",
            "typologies": "Low clock",
            "flags": "Inactif",
            "modules": "2, 3",
            "appel": "Non",
            "note": "Néant",
            "salaire_net": round(row.get("Sales", 0.0) * 0.15, 2),
            "$/h net": 25,
            "Clocked minutes": row.get("Clocked minutes", 0),
            "Scheduled minutes": row.get("Scheduled minutes", 0),
            "Inactivité": row.get("Inactivité", 0),
            "Sales": row.get("Sales", 0.0),
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": row.get("PPVs unlocked", 0),
            "Unlock ratio": convert_percent(row.get("Unlock ratio", "0%")),
            "Golden ratio": convert_percent(row.get("Golden ratio", "0%")),
            "Messages envoyés": row.get("Messages sent", 0),
            "Fans chatted": row.get("Fans chatted", 0),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Reply time": row.get("Reply time", "—"),
            "Tips nets": row.get("Tips Net", 0.0),
            "Messages nets": row.get("Message Net", 0.0),
            "Total earnings": row.get("Total Earnings", 0.0),
            "Nouveaux subs": row.get("New Fans", 0),
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "CA / min": round(row.get("Sales", 0.0) / row.get("Clocked minutes", 1), 4) if row.get("Clocked minutes", 0) > 0 else 0,
            "modules": "2, 3",
            "appel": "Non",

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
            
            "chatteur": row.get("Employees", "-"),
            "modele": row.get("Group", "-"),
            "semaine": "2025-06-23"

            "Sales": row.get("Sales", 0.0),
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": row.get("PPVs unlocked", 0),
            "Unlock ratio": convert_percent(row.get("Unlock ratio", "0%")),
            "Golden ratio": convert_percent(row.get("Golden ratio", "0%")),
            "Messages envoyés": row.get("Messages sent", 0),
            "Fans chatted": row.get("Fans chatted", 0),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Reply time": row.get("Reply time", "—"),
            "Tips nets": row.get("Tips Net", 0.0),
            "Messages nets": row.get("Message Net", 0.0),
            "Total earnings": row.get("Total Earnings", 0.0),
            "Nouveaux subs": row.get("New Fans", 0),
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "chatteur": row.get("Employees", "-"),
            "modele": row.get("Group", "-"),
            "semaine": "2025-06-23",
            "SPC": 85,
            "axe": "Optimiser les conversions",
            "typologies": "Low clock",
            "flags": "Inactif",
            "modules": "2, 3",
            "appel": "Non",
            "note": "Néant",
            "salaire_net": round(row.get("Sales", 0.0) * 0.15, 2),
            "$/h net": 25,
            "Clocked minutes": row.get("Clocked minutes", 0),
            "Scheduled minutes": row.get("Scheduled minutes", 0),
            "Inactivité": row.get("Inactivité", 0),
            "Sales": row.get("Sales", 0.0),
            "PPVs envoyés": row.get("PPVs sent", 0),
            "PPVs débloqués": row.get("PPVs unlocked", 0),
            "Unlock ratio": convert_percent(row.get("Unlock ratio", "0%")),
            "Golden ratio": convert_percent(row.get("Golden ratio", "0%")),
            "Messages envoyés": row.get("Messages sent", 0),
            "Fans chatted": row.get("Fans chatted", 0),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Reply time": row.get("Reply time", "—"),
            "Tips nets": row.get("Tips Net", 0.0),
            "Messages nets": row.get("Message Net", 0.0),
            "Total earnings": row.get("Total Earnings", 0.0),
            "Nouveaux subs": row.get("New Fans", 0),
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "CA / min": round(row.get("Sales", 0.0) / row.get("Clocked minutes", 1), 4) if row.get("Clocked minutes", 0) > 0 else 0,
            "modules": "2, 3",
            "appel": "Non",
            "note": "Néant",
            "salaire_net": salaire_net,
            "$/h net": 25,
            "Clocked minutes": row.get("Clocked hours", 0) * 60 if isinstance(row.get("Clocked hours"), (int, float)) else 0,
            "Prix moyen": round(row.get("Sales", 0.0) / row.get("PPVs unlocked", 1), 2) if row.get("PPVs unlocked", 0) > 0 else 0,
            "CA / fan": round(row.get("Sales", 0.0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,
            "Keystrokes / msg": round(row.get("Keystrokes (words)", 0) / row.get("Messages sent", 1), 2) if row.get("Messages sent", 0) > 0 else 0,
            "CA / min": round(row.get("Sales", 0.0) / row.get("Clocked minutes", 1), 4) if row.get("Clocked minutes", 0) > 0 else 0,
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
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,


        # Simuler l'enregistrement JSON
        print(f"Génération JSON pour {result['chatteur']}: OK")
            "sales": sales,
            "new_subs": creator_row.get("New subscriptions Net") if not creator_row.empty else None,
            "tips_net": creator_row.get("Tips Net") if not creator_row.empty else None,
            "messages_net": creator_row.get("Message Net") if not creator_row.empty else None,
            "earnings_net": creator_row.get("Total earnings Net") if not creator_row.empty else None,
            "ca_modele": creator_row.get("Total earnings Net") if not creator_row.empty else None,
            "fans_modele": creator_row.get("Active fans") if not creator_row.empty else None
        
        "Fans chatted": row.get("Fans chatted"),
            "Messages / fan": round(row.get("Messages sent", 0) / row.get("Fans chatted", 1), 2) if row.get("Fans chatted", 0) > 0 else 0,

    

        # Simuler l'enregistrement JSON
        print(f"Génération JSON pour {result['chatteur']}: OK")
