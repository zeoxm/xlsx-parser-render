import pandas as pd
import os
from datetime import datetime
from utils import (
    convert_time_to_minutes,
    convert_percent,
    safe_divide,
    detect_flags,
    detect_typologies,
    compute_spc,
    compute_coaching_axis
)

def process_files(chatteurs_file, creator_file, temp_dir):
    df_chat = pd.read_excel(chatteurs_file)
    df_creator = pd.read_excel(creator_file)

    df_chat['Golden ratio'] = df_chat['Golden ratio'].apply(convert_percent)
    df_chat['Unlock ratio'] = df_chat['Unlock ratio'].apply(convert_percent)
    df_chat['Scheduled minutes'] = df_chat['Scheduled hours'].apply(convert_time_to_minutes)
    df_chat['Clocked minutes'] = df_chat['Clocked hours'].apply(convert_time_to_minutes)
    df_chat['Inactivité'] = df_chat['Scheduled minutes'] - 40 - df_chat['Clocked minutes']
    df_chat['Prix moyen'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['PPVs unlocked']), axis=1)
    df_chat['CA / fan'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['Fans chatted']), axis=1)
    df_chat['Messages / fan'] = df_chat.apply(lambda row: safe_divide(row['Messages sent'], row['Fans chatted']), axis=1)
    df_chat['Keystrokes / msg'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Messages sent']), axis=1)
    df_chat['Keystrokes / fan'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Fans chatted']), axis=1)
    df_chat['CA / min'] = df_chat.apply(lambda row: safe_divide(row['Sales'], row['Clocked minutes']), axis=1)
    df_chat['Messages / min'] = df_chat.apply(lambda row: safe_divide(row['Messages sent'], row['Clocked minutes']), axis=1)
    df_chat['Keystrokes / min'] = df_chat.apply(lambda row: safe_divide(row['Keystrokes (words)'], row['Clocked minutes']), axis=1)
    df_chat['Salaire brut'] = df_chat['Sales'] * 0.15
    df_chat['Salaire net'] = df_chat['Salaire brut']
    df_chat['Ajustement'] = 0

    ca_total = df_creator['Total earnings Net'].sum()
    fans_total = df_creator['Active fans'].sum()
    nb_chatteurs = len(df_chat)
    semaine = datetime.today().date() - pd.to_timedelta(datetime.today().weekday(), unit='D')
    semaine = semaine.strftime("%Y-%m-%d")

    results = []

    for _, row in df_chat.iterrows():
        chatteur = row['Employees']
        modele = row['Group']
        context = {
            "CA_model": ca_total,
            "fans_model": fans_total,
            "chatteurs_model": nb_chatteurs
        }

        flags = detect_flags(row, context)
        typologies = detect_typologies(row, context)
        spc, spc_details = compute_spc(row, typologies)
        axe, modules, appel = compute_coaching_axis(row, flags, typologies, spc, context)

        result = {
            "chatteur": chatteur,
            "modele": modele,
            "semaine": semaine,
            "SPC": spc,
            "$/h": round(row['CA / min'] * 60, 2),
            "flags": flags,
            "typologies": typologies[:2],
            "axe": axe,
            "modules": modules,
            "appel_managérial": appel,
            "salaire_brut": round(row['Salaire brut'], 2),
            "ajustement": 0,
            "salaire_net": round(row['Salaire net'], 2),
            "CA_model": round(float(str(ca_total).replace(',','.')),2),
            "fans_model": int(fans_total),
        }

        for col in df_chat.columns:
            result[col] = row[col] if not pd.isna(row[col]) else None

        results.append(result)

    return results, semaine
