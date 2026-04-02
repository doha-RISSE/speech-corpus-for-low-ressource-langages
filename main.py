from grammars.cardinal import CardinalFst
from grammars.date import DateFst
from config import CONFIG
from utils import generate_all

cardinal = CardinalFst().fst
date = DateFst(cardinal, CONFIG).fst

text = "15/03/2024"

results = generate_all(text, date)

for r in results:
    print(r)