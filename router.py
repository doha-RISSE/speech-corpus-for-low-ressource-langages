from grammars.money import MoneyFst
from grammars.date_tag import build_date_tagger
from grammars.date_verbalize import build_date_verbalizer


def process_entity(entity, cardinal_fst, config):
    """
    Retourne soit :
      - un FST (pour date) → à composer avec generate_all
      - une liste de strings (pour money) → déjà verbalisé
    """

    if entity["type"] == "date":
        tagger     = build_date_tagger()
        verbalizer = build_date_verbalizer(cardinal_fst, config)
        fst = tagger @ verbalizer
        return {"mode": "fst", "fst": fst}

    elif entity["type"] == "money":
        money_fst = MoneyFst(cardinal_fst, config)
        results   = money_fst.verbalize(entity["value"])
        return {"mode": "list", "results": results}

    else:
        raise ValueError(f"Type d'entité inconnu : {entity['type']}")