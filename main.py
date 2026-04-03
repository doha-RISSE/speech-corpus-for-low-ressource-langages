from grammars.cardinal import CardinalFst
from config import CONFIG
from utils import generate_all

from date_tag import build_date_tagger
from date_verbalize import build_date_verbalizer
from grammars.money import MoneyFst
from grammars.money_verbalize import MoneyVerbalizeFst

# build FSTs
cardinal = CardinalFst().fst

# date
tagger = build_date_tagger()
verbalizer = build_date_verbalizer(cardinal, CONFIG)

# money
money_tagger = MoneyFst(cardinal, CONFIG).fst
money_verbalizer = MoneyVerbalizeFst(cardinal, CONFIG).fst

money_fst = money_tagger @ money_verbalizer

for r in generate_all("200MAD", money_fst):
    print(r)