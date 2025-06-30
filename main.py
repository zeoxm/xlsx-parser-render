from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/parse", methods=["POST"])
def parse():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # TODO: Analyse réelle à injecter ici (mock en attendant)
    data = {
        "prenom": "Charles",
        "modele": "Marie",
        "spc": {
            "score": 78,
            "details": {
                "conversion": 30,
                "effort": 24,
                "exploitable": 24
            },
            "pondération": [40, 30, 30]
        },
        "kpis": {
            "sales_net": 388.0,
            "minutes": 195,
            "fans_actifs": 21,
            "ppv_envoyés": 29,
            "ppv_achetés": 6,
            "unlocks": 6,
            "messages": 168,
            "ppv_ratio": 0.21,
            "unlock_ratio": 0.29,
            "prix_moyen": 3.95,
            "golden_ratio": 0.157,
            "ca_horaire": 119.4
        },
        "flags": {
            "actifs": ["prix moyen trop bas", "volume sans conversion"],
            "silencieux": ["peu de push", "CA horaire instable"]
        },
        "typologies": ["push sec", "volumeur inefficace"],
        "axe": "Travailler la perception de valeur via la montée progressive",
        "modules_recommandés": [3, 10, 13],
        "appel_managérial": {
            "recommandé": True,
            "motif": "Pricing incohérent malgré effort"
        },
        "salaire": {
            "brut": 58.2,
            "ajustement": 0,
            "net": 58.2
        },
        "date_semaine": "2025-07-01",
        "context_model": {
            "traffics_model": "modéré",
            "CA_objectif_chat": 400,
            "statut": "normal",
            "bonus_dispo": False
        }
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
