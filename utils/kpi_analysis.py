
import pandas as pd
from datetime import datetime

def generate_chatters_json(inflow_file, creator_file):
    inflow_df = pd.read_excel(inflow_file)
    creator_df = pd.read_excel(creator_file)
    semaine = datetime.today().strftime('%Y-%m-%d')
    results = []

    for _, row in inflow_df.iterrows():
        prenom = row.get('Prénom')
        modele = row.get('Modèle', 'UNKNOWN')
        sales = row.get('Sales NET', 0)
        clocked = row.get('Clocked minutes', 0)
        messages = row.get('Messages', 0)
        keystrokes = row.get('Keystrokes', 0)
        ppv_envoyes = row.get('PPV envoyés', 0)
        ppv_achetes = row.get('PPV achetés', 0)

        unlock_ratio = round(ppv_achetes / ppv_envoyes, 3) if ppv_envoyes else 0
        prix_moyen = round(sales / ppv_achetes, 2) if ppv_achetes else 0
        ca_horaire = round(sales / (clocked / 60), 2) if clocked else 0
        golden_ratio = round(sales / messages, 3) if messages else 0
        keystroke_ratio = round(keystrokes / messages, 2) if messages else 0

        # Flags
        flags = []
        if unlock_ratio < 0.15: flags.append("Unlock trop bas")
        if prix_moyen < 5: flags.append("Prix PPV trop bas")
        if sales < 100: flags.append("Petit CA")
        if clocked < 120: flags.append("Temps faible")
        if golden_ratio < 0.8: flags.append("Golden ratio faible")

        # Typologies
        typologies = []
        if sales < 100 and clocked > 200: typologies.append("Effort sans résultat")
        if clocked < 60 and sales > 300: typologies.append("Bon pricing, mauvaise présence")
        if unlock_ratio < 0.1 and ppv_envoyes > 20: typologies.append("Pousse dans le vide")
        if prix_moyen > 15 and unlock_ratio > 0.3: typologies.append("Pricing + Conversion")
        if messages > 300 and sales < 50: typologies.append("Bavard inutile")

        # SPC
        spc_conversion = min(unlock_ratio * 100, 100) * 0.4
        spc_effort = min(ca_horaire, 100) * 0.3
        spc_exploitable = min(prix_moyen, 100) * 0.3
        spc_score = round(spc_conversion + spc_effort + spc_exploitable, 2)

        # Axe + modules
        if "Unlock trop bas" in flags: axe = "Mieux doser les pushes"
        elif "Golden ratio faible" in flags: axe = "Mieux cibler les acheteurs"
        elif "Temps faible" in flags: axe = "Mieux s'organiser"
        elif "Prix PPV trop bas" in flags: axe = "Mieux valoriser ses médias"
        else: axe = "Optimiser la stratégie globale"

        modules = []
        if "Unlock trop bas" in flags: modules.append(3)
        if "Prix PPV trop bas" in flags: modules.append(13)
        if "Temps faible" in flags: modules.append(0)
        if "Golden ratio faible" in flags: modules.append(10)

        # Appel
        appel_manag = bool(spc_score < 50 or "Petit CA" in flags)

        # JSON final
        results.append({
            "prenom": prenom,
            "modele": modele,
            "semaine": semaine,
            "kpis": {
                "sales_net": sales,
                "clocked_minutes": clocked,
                "messages": messages,
                "ppv_envoyes": ppv_envoyes,
                "ppv_achetes": ppv_achetes,
                "unlock_ratio": unlock_ratio,
                "prix_moyen": prix_moyen,
                "ca_horaire": ca_horaire,
                "golden_ratio": golden_ratio,
                "keystrokes_ratio": keystroke_ratio
            },
            "spc": {
                "score": spc_score,
                "details": {
                    "conversion": round(spc_conversion, 2),
                    "effort": round(spc_effort, 2),
                    "exploitable": round(spc_exploitable, 2)
                },
                "pondération": [40, 30, 30]
            },
            "flags": flags,
            "typologies": typologies[:2],
            "axe_coaching": axe,
            "modules_recommandes": modules,
            "appel_managérial": appel_manag,
            "salaire": {
                "brut": round(sales * 0.15, 2),
                "ajustement": 0,
                "net": round(sales * 0.15, 2)
            }
        })

    return results
