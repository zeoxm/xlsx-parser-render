
def enrich_row(row):
    sales = row.get("Sales", 0.0)
    prix_moyen = row.get("Prix moyen", 0.0)
    ca_fan = row.get("CA / fan", 0.0)
    unlock = row.get("Unlock ratio", 0.0)
    golden = row.get("Golden ratio", 0.0)
    clocked = row.get("Clocked minutes", 0)
    kpm = row.get("Keystrokes / msg", 0.0)
    mpm = row.get("Messages / min", 0.0)
    inact = row.get("Inactivité", 0)
    fans = row.get("Fans chatted", 1)
    messages = row.get("Messages envoyés", 0)

    # --- SPC ---
    spc = 0
    spc += 10 if unlock >= 35 else 5 if unlock >= 25 else 0
    spc += 10 if prix_moyen > 25 else 5 if prix_moyen >= 20 else 0
    spc += 10 if ca_fan > 2 else 5 if ca_fan >= 1 else 0
    spc += 10 if 3 <= golden <= 5 else 5 if 2 <= golden < 3 or 5 < golden <= 6 else 0
    spc += 10 if clocked > 1800 else 5 if clocked >= 1200 else 0
    spc += 10 if 40 <= kpm <= 60 else 5 if 25 <= kpm < 40 or 60 < kpm <= 70 else 0
    spc += 5 if mpm > 1.1 else 3 if mpm >= 0.7 else 0
    spc += 5 if inact < 40 else 3 if inact <= 60 else 0
    spc += 10 if sales < 100 else 0
    spc = min(spc, 100)
    row["SPC"] = spc

    # --- Typologies ---
    typologies = []
    if messages > 4000 and sales < 200 and unlock < 25:
        typologies.append("Volumeur inefficace")
    if unlock > 40 and prix_moyen < 20:
        typologies.append("Unlocker low cost")
    if sales > 300 and messages < 1500 and unlock > 30:
        typologies.append("Sniper rentable")
    if clocked > 300 and sales < 300:
        typologies.append("Présent non rentable")
    if sales > 500 and clocked < 180:
        typologies.append("Sous-exploité")
    if clocked > 0 and inact > 60:
        typologies.append("Ghost partiel")
    row["typologies"] = ", ".join(typologies[:2]) if typologies else "-"

    # --- Flags ---
    flags = []
    if unlock < 20:
        flags.append("F3")
    if golden > 6 and unlock < 25:
        flags.append("F2")
    if prix_moyen < 15:
        flags.append("F4")
    if clocked == 0 or inact > 60:
        flags.append("F1")
    if messages > 4000 and fans < 100:
        flags.append("F7")
    if kpm > 70:
        flags.append("F10")
    row["flags"] = ", ".join(flags) if flags else "-"

    # --- Axe coaching & Modules ---
    axe = "-"
    modules = set()
    if "F1" in flags:
        axe = "Présence instable ou absente"
        modules.update(["0"])
    elif "F3" in flags or unlock < 25:
        axe = "Push inefficace ou mal timé"
        modules.update(["3", "4", "14"])
    elif "F4" in flags:
        axe = "Contenu sous-valorisé"
        modules.update(["13", "6"])
    elif "F7" in flags:
        axe = "Mauvaise gestion des leads"
        modules.update(["5", "3"])
    elif "F10" in flags:
        axe = "Style automatisé suspect"
        modules.update(["9", "12"])
    elif "Volumeur inefficace" in typologies:
        axe = "Trop d’effort pour peu de résultats"
        modules.update(["3", "14", "4"])
    row["axe"] = axe
    row["modules"] = ", ".join(sorted(modules)) if modules else "-"

    # --- Appel managérial ---
    appel = "Oui" if "F1" in flags or spc < 45 or "Volumeur inefficace" in typologies else "Non"
    row["appel"] = appel

    # --- Note libre ---
    row["note"] = "-"

    return row
