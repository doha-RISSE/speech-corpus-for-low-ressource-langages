import re
from detector import detect_entities
from router import process_entity
from grammars.cardinal import CardinalFst
from config import CONFIG
from utils import generate_all


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _verbalize_cardinal_isolated(text, cardinal_fst):
    """
    Cherche tous les nombres isolés dans le texte (qui ne font pas partie
    d'une date ou d'une expression monétaire déjà détectée) et les remplace
    par leurs verbalisations.
    Retourne une liste de toutes les combinaisons possibles.
    """
    # On trouve tous les nombres isolés (entiers seulement pour le cardinal)
    number_re = re.compile(r"\b(\d+)\b")
    tokens = number_re.split(text)
    # tokens alterne : [texte, nombre, texte, nombre, ...]

    candidates_per_slot = []
    for i, tok in enumerate(tokens):
        if i % 2 == 1:  # c'est un nombre
            verbals = generate_all(tok, cardinal_fst)
            candidates_per_slot.append(verbals if verbals else [tok])
        else:
            candidates_per_slot.append([tok])   # texte fixe

    # Produit cartésien de tous les slots
    results = [""]
    for slot in candidates_per_slot:
        results = [prev + s for prev in results for s in slot]

    return results


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def normalize(text, cardinal_only=False):
    """
    Normalise le texte brut en Darija verbalisé.

    Paramètres
    ----------
    text : str
        Texte brut d'entrée.
    cardinal_only : bool
        Si True, on ne fait que la verbalization des nombres isolés
        (utile pour tester CardinalFst indépendamment).

    Retourne
    --------
    list[str]
        Toutes les verbalisations possibles du texte.
    """
    cardinal_fst = CardinalFst().fst

    # --- Mode cardinal isolé uniquement ---
    if cardinal_only:
        return _verbalize_cardinal_isolated(text, cardinal_fst)

    # --- Mode normal : détection d'entités (date, money) ---
    entities = detect_entities(text)

    # Si aucune entité détectée → on tente le cardinal isolé
    if not entities:
        return _verbalize_cardinal_isolated(text, cardinal_fst)

    results = [""]
    last    = 0

    for e in entities:
        prefix = text[last:e["start"]]

        output = process_entity(e, cardinal_fst, CONFIG)

        if output["mode"] == "fst":
            candidates = generate_all(e["value"], output["fst"])
            if not candidates:
                candidates = [e["value"]]   # fallback
        else:
            candidates = output["results"]

        # Produit cartésien : chaque résultat précédent × chaque candidat
        results = [prev + prefix + c for prev in results for c in candidates]

        last = e["end"]

    # Texte restant après la dernière entité
    suffix = text[last:]
    results = [r + suffix for r in results]

    return list(set(results))


# ---------------------------------------------------------------------------
# Test rapide
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        " عندي موعد 12/05/2026",       # date
        " شريت هاد البيسي ب 8500 درهم",  # money entier
        " خلصت 8500.50 MAD",            # money décimal
        " € 250 هي التمن",              # money devise avant
        " عندي 3 ديال الولاد",           # cardinal isolé
        " عندي موعد 12/05/2026 وخلصت 8500 درهم",  # date + money
    ]

    for t in tests:
        print(f"\nInput  : {t}")
        results = normalize(t)
        for r in results:
            print(f"  → {r}")