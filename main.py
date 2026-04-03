from grammars.cardinal import CardinalFst
from config import CONFIG
from utils import generate_all

from date_tag import build_date_tagger
from date_verbalize import build_date_verbalizer

# build FSTs
cardinal = CardinalFst().fst
tagger = build_date_tagger()
verbalizer = build_date_verbalizer(cardinal, CONFIG)

# compose
fst = tagger @ verbalizer

# test
text = "01/07/2024"

results = generate_all(text, fst)

for r in results:
    print(r)