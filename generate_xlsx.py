import pandas as pd

def generate_synthese_manager(json_data_list, output_path):
    rows = []

    for data in json_data_list:
        row = {
            "Chatteur": data.get("chatteur"),
            "Modèle": data.get("modele"),
            "SPC": data.get("SPC"),
            "$/h net": data.get("dollars_per_hour", 0),
            "Typologies": data.get("typologies"),
            "Flags": data.get("flags"),
            "Axe": data.get("axe"),
            "Modules": data.get("modules"),
            "Appel ?": data.get("appel"),
            "Salaire net": round(data.get("salaire_net", 0), 2),
            "Ajustement": round(data.get("ajustement", 0), 2),
            "CA modèle": round(data.get("ca_modele", 0), 2),
            "Fans modèle": data.get("fans_modele", 0),
            "Semaine": data.get("semaine")
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
