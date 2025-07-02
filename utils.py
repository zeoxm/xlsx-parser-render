import pandas as pd
import re

import re

def convert_time_to_minutes(time_str):
    if pd.isna(time_str):
        return 0

    time_str = str(time_str).lower().replace(" ", "")

    hours = 0
    minutes = 0

    match_hours = re.search(r'(\d+)h', time_str)
    match_minutes = re.search(r'(\d+)min', time_str)

    if match_hours:
        hours = int(match_hours.group(1))
    if match_minutes:
        minutes = int(match_minutes.group(1))

    return hours * 60 + minutes

def convert_percent(value):
    try:
        return float(str(value).replace('%', '').replace(',', '.')) / 100
    except:
        return 0

def safe_divide(a, b):
    try:
        if b == 0 or b is None:
            return 0
        return float(a) / float(b)
    except:
        return 0

def detect_flags(row, context):
    flags = []
    if row['Unlock ratio'] < 0.20:
        flags.append('F1 - Unlock trop bas')
    if row['Golden ratio'] > 6 and row['Unlock ratio'] < 0.25:
        flags.append('F2 - Push trop violent')
    if row['Prix moyen'] < 4:
        flags.append('F3 - Prix trop bas')
    if row['Clocked minutes'] == 0 or row['Inactivité'] > 60:
        flags.append('F4 - Inactif ou absent')
    return flags

def detect_typologies(row, context):
    types = []
    if row['Messages sent'] > 6000 and row['Sales'] < 300:
        types.append("Volumeur inefficace")
    if row['Unlock ratio'] > 0.40 and row['Prix moyen'] < 6:
        types.append("Unlocker low cost")
    if row['Golden ratio'] > 6 and row['Unlock ratio'] < 0.25:
        types.append("Script brutal")
    if row['Keystrokes (words)'] > 3000 and row['Sales'] < 200:
        types.append("Relationnel non vendeur")
    if row['Clocked minutes'] < 200 and row['Sales'] > 300:
        types.append("Ghost performer")
    return types

def compute_spc(row, typologies):
    score = 0
    if row['Unlock ratio'] >= 0.3:
        score += 10
    if 4 <= row['Golden ratio'] <= 5:
        score += 10
    if row['Sales'] >= 300:
        score += 10
    if row['Prix moyen'] >= 15:
        score += 10
    if row['Messages sent'] >= 3000:
        score += 10
    if row['Keystrokes (words)'] >= 2000:
        score += 10
    if row['Clocked minutes'] >= 400:
        score += 10
    if 'Volumeur inefficace' in typologies or 'Relationnel non vendeur' in typologies:
        score += 15
    if 'Unlocker low cost' in typologies:
        score += 15
    return min(score, 100), {"debug_score": score}

def compute_coaching_axis(row, flags, typologies, spc, context):
    axe = ""
    modules = []
    appel = "Non"
    if 'Volumeur inefficace' in typologies:
        axe = "Tu bosses énormément mais tes ventes sont faibles. On va restructurer tes messages pour que ça vende."
        modules = [3, 4, 10]
        appel = "Oui"
    elif 'Script brutal' in typologies:
        axe = "Tu envoies trop de pushs trop secs. On doit retravailler la progression."
        modules = [3, 4, 14]
        appel = "Oui"
    elif 'Unlocker low cost' in typologies:
        axe = "Tu vends beaucoup mais à très petit prix. Il faut valoriser tes contenus."
        modules = [6, 13, 14]
    elif 'Ghost performer' in typologies:
        axe = "Tu bosses peu mais t’as du potentiel de sniper. Si tu montes en rythme, t’exploses tout."
        modules = [0, 3]
    elif 'Relationnel non vendeur' in typologies:
        axe = "Ton style est riche mais ça ne convertit pas. Il faut retravailler les relances."
        modules = [5, 6, 10]
    if spc < 40 or row['Inactivité'] > 200 or 'F4 - Inactif ou absent' in flags:
        appel = "Oui"
    return axe, modules, appel
