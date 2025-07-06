def process_files(chatteurs_path, creator_path, output_dir):
    df_chat = clean_columns(pd.read_excel(chatteurs_path))
    df_creator = clean_columns(pd.read_excel(creator_path))
    # ...
    for index, row in df_chat.iterrows():
        employee = row.get("Employees", None)
        if not isinstance(employee, str):
            employee = str(employee) if employee is not None else f"inconnu_{index}"
            employee = employee.strip()
        if not employee or employee.lower() in ["none", "nan", "false"]:
            employee = f"inconnu_{index}"
        # ... autres traitements ici, bien indentés ...
        # Fin de la boucle for
    # Fin de la fonction
