from grammars.money import MoneyFst
from grammars.date import DateFst

FST_MAP = {
    "money": MoneyFst,
    "date": DateFst
}


def process_entity(entity, cardinal, config):
    fst_class = FST_MAP[entity["type"]]
    fst = fst_class(cardinal, config).fst

    return entity["value"] @ fst