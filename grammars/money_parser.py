import re

NUMBER_PATTERN = r"(\d+(?:[.,]\d+)?)"


def _build_currency_regex(currencies: dict) -> str:
    """
    Construit dynamiquement le pattern regex des devises
    depuis le dict config["money"]["currencies"].
    Les symboles spéciaux regex sont échappés automatiquement.
    Trie par longueur décroissante pour que "MAD" matche avant "M".
    """
    symbols = sorted(currencies.keys(), key=len, reverse=True)
    escaped = [re.escape(s) for s in symbols]
    return "(" + "|".join(escaped) + ")"


def parse_money(text: str, currencies: dict):
    """
    Extrait (montant_str, devise_verbalisée) depuis n'importe quel format.
    Utilise le dict currencies de config pour la reconnaissance et la traduction.

    Retourne (None, None) si rien trouvé.
    """
    text            = re.sub(r"\s+", " ", text.strip())
    currency_re     = _build_currency_regex(currencies)

    # Cas 1 : nombre AVANT devise   (8500 درهم | 8500.50 MAD)
    m = re.search(rf"{NUMBER_PATTERN}\s*{currency_re}", text)
    if m:
        return _clean(m.group(1)), currencies.get(m.group(2), m.group(2))

    # Cas 2 : devise AVANT nombre   (MAD 8500 | € 250)
    m = re.search(rf"{currency_re}\s*{NUMBER_PATTERN}", text)
    if m:
        return _clean(m.group(2)), currencies.get(m.group(1), m.group(1))

    # Fallback : nombre seul → devise par défaut درهم
    m = re.search(NUMBER_PATTERN, text)
    if m:
        return _clean(m.group(1)), "درهم"

    return None, None


def _clean(amount_str: str) -> str:
    """Normalise la virgule en point décimal."""
    return amount_str.replace(",", ".")