import re
from detector import detect_entities
from router import process_entity
from grammars.cardinal import CardinalFst, verbalize_number
from config import CONFIG
from utils import generate_all
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_cardinal_fst():
    """Instance unique de CardinalFst, construite une seule fois."""
    return CardinalFst(CONFIG)


def _verbalize_cardinal_isolated(text: str) -> list:
    number_re = re.compile(r"\b(\d+)\b")
    tokens    = number_re.split(text)

    slots = []
    for i, tok in enumerate(tokens):
        if i % 2 == 1:
            slots.append([verbalize_number(tok)])
        else:
            slots.append([tok])

    results = [""]
    for slot in slots:
        results = [prev + s for prev in results for s in slot]
    return results


def normalize(text: str, cardinal_only: bool = False) -> list:
    cardinal_fst_obj = _get_cardinal_fst()

    if cardinal_only:
        return _verbalize_cardinal_isolated(text)

    entities = detect_entities(text)

    if not entities:
        return _verbalize_cardinal_isolated(text)

    results = [""]
    last    = 0

    for e in entities:
        prefix = text[last:e["start"]]
        output = process_entity(e, cardinal_fst_obj, CONFIG)

        if output["mode"] == "fst":
            candidates = generate_all(e["value"], output["fst"]) or [e["value"]]
        else:
            candidates = output["results"]

        results = [prev + prefix + c for prev in results for c in candidates]
        last = e["end"]

    suffix  = text[last:]
    results = [r + suffix for r in results]

    return list(set(results))


if __name__ == "__main__":
    tests = [
        (" عندي موعد 12/05/2026",                 "date"),
        (" شريت هاد البيسي ب 8500 درهم",          "money entier"),
        (" خلصت 8500.50 MAD",                      "money décimal"),
        (" € 250 هي التمن",                        "money devise avant"),
        (" شريت ب 8500,50 EUR",                    "money virgule + EUR"),
        (" عندي 3 ديال الولاد",                    "cardinal isolé"),
        (" عندي موعد 12/05/2026 وخلصت 8500 درهم", "date + money"),
    ]

    for text, label in tests:
        print(f"\n[{label}]  {text.strip()}")
        for r in normalize(text):
            print(f"   → {r}")