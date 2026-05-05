import re

# Tous les symboles/mots de devise
CURRENCY_PATTERN = r"(MAD|د\.م|€|\$|درهم|أورو|دولار)"

# Mapping devise → verbalisation en Darija
CURRENCY_VERBAL = {
    "MAD":   "درهم",
    "د.م":   "درهم",
    "€":     "أورو",
    "$":     "دولار",
    "درهم":  "درهم",
    "أورو":  "أورو",
    "دولار": "دولار",
}

# Nombre entier ou décimal (virgule ou point)
NUMBER_PATTERN = r"(\d+(?:[.,]\d+)?)"


def parse_money(text):
    """
    Extrait (montant_str, devise_verbalisee) depuis n'importe quel format :
      8500 درهم | 8500.50 MAD | MAD 8500 | € 250 | درهم8500 ...
    Retourne (None, None) si rien trouvé.
    """
    text = re.sub(r"\s+", " ", text.strip())

    # --- Cas 1 : nombre AVANT devise ---
    m = re.search(rf"{NUMBER_PATTERN}\s*{CURRENCY_PATTERN}", text)
    if m:
        amount_raw = m.group(1)
        currency_raw = m.group(2)
        return _clean_amount(amount_raw), CURRENCY_VERBAL.get(currency_raw, currency_raw)

    # --- Cas 2 : devise AVANT nombre ---
    m = re.search(rf"{CURRENCY_PATTERN}\s*{NUMBER_PATTERN}", text)
    if m:
        currency_raw = m.group(1)
        amount_raw = m.group(2)
        return _clean_amount(amount_raw), CURRENCY_VERBAL.get(currency_raw, currency_raw)

    # --- Fallback : nombre seul ---
    m = re.search(NUMBER_PATTERN, text)
    if m:
        return _clean_amount(m.group(1)), "درهم"

    return None, None


def _clean_amount(amount_str):
    """
    Normalise le séparateur décimal → point.
    Ex : "8500,50" → "8500.50"
    """
    return amount_str.replace(",", ".")