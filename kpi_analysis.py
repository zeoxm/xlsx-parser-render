def process_files(chatteurs_path, creator_path, output_dir):
    # ...
    for index, row in df_chat.iterrows():
        employee = row.get("Employees", None)
        # ... votre logique de récupération d'employee ...

        # Toute votre logique métier (calculs spc, typologies, flags, etc.)
        spc = 0
        spc += 10 if unlock >= 35 else 5 if unlock >= 25 else 0
        # ... etc ...

        # Suite du traitement, puis :
        result = enrich_row(result)
        # ... sauvegarde JSON ...
