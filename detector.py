import re
from config import CONFIG

NUMBER = r"\d+(?:[.,]\d+)?"


def _build_money_pattern(currencies: dict) -> str:
    """
    Construit le pattern money depuis config["money"]["currencies"].
    Trie par longueur décroissante pour éviter les faux matchs partiels.
    """
    symbols = sorted(currencies.keys(), key=len, reverse=True)
    escaped = [re.escape(s) for s in symbols]
    cur     = "(" + "|".join(escaped) + ")"
    return (
        rf"\b{NUMBER}\s*{cur}\b"   # 8500 درهم | 8500.50 MAD
        rf"|{cur}\s*{NUMBER}\b"    # MAD 8500  | € 250
    )


def _build_patterns() -> dict:
    """
    Construit le dict PATTERNS depuis CONFIG.
    Ajouter une classe dans CONFIG → elle apparaît automatiquement ici
    si elle a un champ "pattern" (classes statiques) ou est connue ici.
    """
    patterns = {}

    # Money : pattern généré depuis la liste de devises
    if "money" in CONFIG:
        patterns["money"] = _build_money_pattern(CONFIG["money"]["currencies"])

    # Date : pattern fixe JJ/MM/AAAA
    if "date" in CONFIG:
        patterns["date"] = r"\b\d{1,2}/\d{1,2}/\d{4}\b"
    # Numéro de téléphone marocain : 06/07/05 + 8 chiffres
    if "phone" in CONFIG:
        patterns["phone"] = r"\b0[5-7]\d{8}\b"

    # Pourcentage : nombre suivi de %
    if "percent" in CONFIG:
        patterns["percent"] = r"\b\d+(?:[.,]\d+)?\s*%"
    if "time" in CONFIG:
        patterns["time"] = r"\b([0-2]?[0-9])[:hH]([0-5][0-9])\b"

    # --- Classes futures : ajouter leur pattern ici ---
    # if "time" in CONFIG:
    #     patterns["time"] = r"\b\d{1,2}:\d{2}\b"
    #
    # if "phone" in CONFIG:
    #     patterns["phone"] = r"\b0[5-7]\d{8}\b"

    return patterns


PATTERNS = _build_patterns()


def detect_entities(text: str) -> list:
    entities = []
    for label, pattern in PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities.append({
                "type":  label,
                "value": m.group(),
                "start": m.start(),
                "end":   m.end(),
            })
    return sorted(entities, key=lambda x: x["start"])