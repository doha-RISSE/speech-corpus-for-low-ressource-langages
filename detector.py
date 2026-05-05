import re

# Tous les symboles de devises supportés
CURRENCY_SYMBOLS = r"(MAD|د\.م|€|\$|درهم|أورو|دولار)"

# Nombre entier ou décimal
NUMBER = r"\d+(?:[.,]\d+)?"

PATTERNS = {
    # money : toutes les combinaisons (nombre avant/après devise, avec/sans espace)
    "money": (
        rf"\b{NUMBER}\s*{CURRENCY_SYMBOLS}\b"   # 8500درهم / 8500 درهم / 8500.50 MAD
        rf"|{CURRENCY_SYMBOLS}\s*{NUMBER}\b"    # درهم8500 / MAD 8500 / € 250
    ),
    # date : JJ/MM/AAAA
    "date": r"\b\d{1,2}/\d{1,2}/\d{4}\b",
}


def detect_entities(text):
    entities = []

    for label, pattern in PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities.append({
                "type":  label,
                "value": m.group(),
                "start": m.start(),
                "end":   m.end()
            })

    # Trier par position dans le texte
    return sorted(entities, key=lambda x: x["start"])