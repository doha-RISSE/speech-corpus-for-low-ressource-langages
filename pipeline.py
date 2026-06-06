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
        ("عافاك يلا وصلتي للدار عيط ليا فهاد الرقم: 0612345678.", "numéro de téléphone"),
        ("الصولد هاد السيمانة واصل تال 50% فكاع الحوايج.", " %"),
        ("نسبة النجاح فهاد الامتحان هي 99.9%.", " % avec virgule "),
        ("الطيارة غادا تقلع مع 08:00 ديال الصباح.", "time"),
        ("نتلاقاو مع 10:10 ولا 10:15 حدا البوسطة.", "time"),
        ("الماتش غادي يبدا مع 20:30.", "time"),
        ("وصلت للخدمة مع 08:45 ودخلت للاجتماع مع 09:50.", "time"),
        ("بقيت سهران خدام تال 00:00 عاد نعست.", "time"),
        ("التران ديال 14:12 ديما كيتعطل.", "time"),
        ("جا عندي مع 16:20 ومشا بحالو مع 17:55.", "time"),
        ("وصلت مع 10:01 للخدمة.", "time"),
        ("بقات 14:04 ويسد البنكة.", "time"),
        ("التران غادي يخرج مع 16:23.", "time"),
        ("الاجتماع غادي يسالي مع 08:45.", "time"),






    ]

    for text, label in tests:
        print(f"\n[{label}]  {text.strip()}")
        for r in normalize(text):
            print(f"   → {r}")