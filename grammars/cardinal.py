import pynini
from .base import GraphFst

def nombre_vers_darija(n):
    # simplifié (tu peux garder ton code)
    return str(n)

class CardinalFst(GraphFst):
    def __init__(self, max_number=3000):
        super().__init__("cardinal")

        pairs = []
        for i in range(1, max_number):
            pairs.append((str(i), nombre_vers_darija(i)))
            if i < 10:
                pairs.append((f"0{i}", nombre_vers_darija(i)))

        self.fst = pynini.string_map(pairs).optimize()