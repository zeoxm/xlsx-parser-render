import pandas as pd

def generate_synthese_manager(json_data_list, output_path):
    rows = []
    for data in json_data_list:
        row = {
            "Chatteur": data.get("chatteur"),
            "Modèle": data.get("modele"),
            "SPC": data.get("SPC"),
            "Sales NET": round(data.get("Sales") or 0, 2),
            "$/h": data.get("$/h"),
            "Typo 1": data.get("typologies")[0] if data.get("typologies") else "",
            "Typo 2": data.get("typologies")[1] if len(data.get("typologies")) > 1 else "",
            "Flags": ", ".join(data.get("flags")) if data.get("flags") else "",
            "Axe": data.get("axe"),
            "Modules": ", ".join([str(m) for m in data.get("modules")]) if data.get("modules") else "",
            "Salaire brut": round(data.get("salaire_brut") or data.get ("salaire") or 0, 2),
            "Ajustement": data.get("ajustement", 0),
            "Salaire net": round(data.get("salaire_net") or data.get ("salaire") or 0, 2),
            "Appel ?": data.get("appel_managérial")
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
