
# XLSX Parser Render API

Cette API hébergée sur Render exécute toute la phase 6 du plan d’automatisation :
- Parse les exports
- Génère les JSON par c...
- Produit les rapports DOCX et PDF
- Crée la Synthèse Manager XLSX
- Met à jour les JSON selon les ajustements
- Génère les rapports finaux

## Endpoints

- `POST /parse` : Recevoir 2 fichiers `.xlsx`, retourne les `.json`
- `POST /generate-docx` : Reçoit JSON, retourne fichier `.docx`
- `POST /generate-pdf` : Reçoit JSON ou `.docx`, retourne `.pdf`
- `POST /generate-xlsx` : Reçoit JSON list, retourne manager `.xlsx`
- `POST /update-json-with-adjustments` : Reçoit JSON + XLSX, retourne nouveaux JSON
- `POST /finalize-reports` : Reçoit JSON ajustés, retourne PDF finaux
