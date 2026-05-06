from grammars.date_tag import build_date_tagger
from grammars.date_verbalize import build_date_verbalizer
from grammars.money import MoneyFst


def process_entity(entity: dict, cardinal_fst, config: dict) -> dict:

    if entity["type"] == "date":
        tagger     = build_date_tagger()
        verbalizer = build_date_verbalizer(cardinal_fst.build_fst_for_date(), config)
        return {"mode": "fst", "fst": tagger @ verbalizer}

    elif entity["type"] == "money":
        # money.py appelle generate_all() qui a besoin du FST
        fst     = cardinal_fst.build_fst_for_date()
        results = MoneyFst(fst, config).verbalize(entity["value"])
        return {"mode": "list", "results": results}

    else:
        raise ValueError(f"Type d'entité inconnu : {entity['type']}")